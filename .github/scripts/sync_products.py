#!/usr/bin/env python3
"""Keep crawlable portfolio navigation and homepage product schema synchronized."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = json.loads((ROOT / 'content/products.json').read_text())


def update(source, relative):
    if '<header' not in source:
        return source
    def primary(match):
        opening, body, closing = match.groups()
        if 'href="/salvera/"' not in body:
            link = '<a href="/salvera/">Salvera</a>'
            temvica = re.search(r'<a\b[^>]*href="/temvica/"[^>]*>.*?</a>', body, re.S)
            if temvica:
                body = body[:temvica.end()] + '\n        ' + link + body[temvica.end():]
            else:
                body = body.rstrip() + '\n        ' + link + '\n      '
        if relative.startswith('salvera/'):
            current = 'page' if relative == 'salvera/index.html' else 'location'
            body = re.sub(r'<a\b[^>]*href="/salvera/"[^>]*>', f'<a href="/salvera/" aria-current="{current}">', body)
        return opening + body + closing
    source = re.sub(r'(<nav\b[^>]*class="nav-links"[^>]*>)(.*?)(</nav>)', primary, source, flags=re.S)
    def footer(match):
        body = match[0]
        for product in CATALOG['products']:
            if f'href="{product["path"]}"' not in body:
                body = body.replace('</ul>', f'<li><a href="{product["path"]}">{product["name"]}</a></li></ul>')
        return body
    source = re.sub(r'<nav\b[^>]*class="footer-col"[^>]*aria-label="Products"[^>]*>.*?</nav>', footer, source, flags=re.S)
    if relative == 'index.html':
        def schema(match):
            data = json.loads(match[2])
            if data.get('@type') != 'ItemList': return match[0]
            data['numberOfItems'] = len(CATALOG['products'])
            data['itemListElement'] = [{'@type': 'ListItem', 'position': i, 'name': p['name'], 'url': CATALOG['origin'] + p['path']} for i, p in enumerate(CATALOG['products'], 1)]
            return match[1] + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n' + match[3]
        source = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', schema, source, flags=re.S)
    return source


def sync(check=False):
    changed = []
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' in path.parts or '.github' in path.parts or path.name.startswith('google'): continue
        source = path.read_text()
        result = update(source, path.relative_to(ROOT).as_posix())
        if result != source:
            changed.append(str(path.relative_to(ROOT)))
            if not check: path.write_text(result)
    if check and changed: raise SystemExit('Run sync_products.py: ' + ', '.join(changed))
    print(f'PASS: product navigation/schema synchronized; {len(changed)} changed pages' if check else f'Synchronized product navigation/schema on {len(changed)} pages')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true')
    sync(parser.parse_args().check)
