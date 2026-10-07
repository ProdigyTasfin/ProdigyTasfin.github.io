#!/usr/bin/env python3
"""Validate static Pages sources without installing third-party dependencies."""
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = 'https://nextflow-apps.com'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids, self.references, self.canonicals = [], [], []
        self.scripts, self.metadata = [], {}
        self.refreshes = []
        self.h1_count = 0
        self.script = None
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'meta':
            self.metadata[a.get('name', a.get('property', ''))] = a.get('content', '')
            if a.get('http-equiv', '').lower() == 'refresh':
                self.refreshes.append(a.get('content', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href', ''))
        if tag == 'a' or (tag == 'link' and a.get('rel') in ('stylesheet', 'icon', 'apple-touch-icon')):
            self.references.append(a.get('href', ''))
        if tag in ('img', 'script', 'iframe', 'source'):
            if 'src' in a:
                self.references.append(a['src'])
        if tag == 'script':
            self.script = (a, [])

    def handle_data(self, data):
        if self.script is not None:
            self.script[1].append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            a, chunks = self.script
            self.scripts.append((a, ''.join(chunks)))
            self.script = None


def page_url(path):
    relative = path.relative_to(ROOT).as_posix()
    return ORIGIN + '/' + (relative[:-10] if relative.endswith('index.html') else relative)


def check_site():
    failures = []
    paths = sorted(path for path in ROOT.rglob('*.html') if '.git' not in path.parts and '.github' not in path.parts)
    pages = {path: Page(path.read_text()) for path in paths}
    redirects = json.loads((ROOT / 'content/redirects.json').read_text())
    aliases = {ROOT / alias.lstrip('/') / 'index.html': target for alias, target in redirects.items()}
    for missing in set(aliases) - set(pages):
        failures.append(f'Missing redirect fallback: {missing.relative_to(ROOT)}')
    public = {path: page for path, page in pages.items() if not path.name.startswith('google') and path.name != '404.html' and path not in aliases}
    for path, page in pages.items():
        label = path.relative_to(ROOT).as_posix()
        for ident, count in Counter(page.ids).items():
            if count > 1:
                failures.append(f'{label}: duplicate ID {ident}')
        for ref in page.references:
            u = urlsplit(ref)
            if u.scheme and (u.scheme != 'https' or u.netloc != urlsplit(ORIGIN).netloc):
                continue
            if u.netloc and u.netloc != urlsplit(ORIGIN).netloc:
                continue
            target = ROOT / unquote(u.path.lstrip('/')) if u.path.startswith('/') else path.parent / unquote(u.path)
            if not u.path:
                target = path
            target = target.resolve()
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(ROOT) or not target.is_file():
                failures.append(f'{label}: missing local target {ref}')
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                failures.append(f'{label}: missing fragment {ref}')
        if path in public:
            expected = page_url(path)
            if page.canonicals != [expected]:
                failures.append(f'{label}: canonical should be {expected}')
            if page.h1_count != 1 or not page.metadata.get('description'):
                failures.append(f'{label}: needs one H1 and a description')
            if page.metadata.get('og:url', expected) != expected:
                failures.append(f'{label}: Open Graph URL differs from canonical')
            main_scripts = [a for a, _ in page.scripts if a.get('src') == '/assets/js/main.js']
            if len(main_scripts) != 1:
                failures.append(f'{label}: needs exactly one shared navigation script')
            if page.refreshes or any(word in page.metadata.get('robots', '').lower() for word in ('noindex', 'nofollow')):
                failures.append(f'{label}: public page must be indexable without redirects')
        elif path in aliases:
            destination = ORIGIN + aliases[path]
            if page.refreshes != [f'0; url={destination}'] or page.canonicals != [destination] or page.metadata.get('robots') != 'noindex, follow':
                failures.append(f'{label}: invalid static redirect fallback')
            if aliases[path] in redirects or not (ROOT / aliases[path].lstrip('/') / 'index.html').is_file():
                failures.append(f'{label}: redirect target missing or chained')
        elif path.name == '404.html':
            if page.canonicals or page.metadata.get('robots') != 'noindex, follow' or page.h1_count != 1:
                failures.append('404.html: needs one H1, noindex and no canonical')
        for a, source in page.scripts:
            if a.get('type') == 'application/ld+json':
                try:
                    json.loads(source)
                except ValueError as exc:
                    failures.append(f'{label}: invalid JSON-LD: {exc}')
            elif not a.get('src') and a.get('type', '') in ('', 'module', 'text/javascript'):
                with tempfile.NamedTemporaryFile(suffix='.js', mode='w') as temporary:
                    temporary.write(source)
                    temporary.flush()
                    result = subprocess.run(['node', '--check', temporary.name], capture_output=True, text=True)
                if result.returncode:
                    failures.append(f'{label}: invalid inline JavaScript: {result.stderr}')
    for script in (ROOT / 'assets/js').glob('*.js'):
        result = subprocess.run(['node', '--check', str(script)], capture_output=True, text=True)
        if result.returncode:
            failures.append(f'{script.relative_to(ROOT)}: {result.stderr}')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    locations = [item.text for item in sitemap.findall('.//s:loc', ns)]
    expected = {page_url(path) for path in public}
    if len(locations) != len(set(locations)) or set(locations) != expected:
        failures.append(f'Sitemap mismatch: missing {expected - set(locations)}, extra {set(locations) - expected}')
    if f'Sitemap: {ORIGIN}/sitemap.xml' not in (ROOT / 'robots.txt').read_text():
        failures.append('robots.txt must advertise the sitemap')
    if (ROOT / 'CNAME').read_text().strip() != urlsplit(ORIGIN).netloc or not (ROOT / '.nojekyll').exists():
        failures.append('Pages requires the expected CNAME and .nojekyll marker')
    for association in (ROOT / '.well-known').glob('*.json'):
        json.loads(association.read_text())
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'PASS: {len(public)} public pages; links, anchors, metadata, JSON-LD, JavaScript, sitemap and Pages markers.')
    return 0


if __name__ == '__main__':
    sys.exit(check_site())
