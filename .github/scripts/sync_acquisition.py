#!/usr/bin/env python3
"""Render crawlable CTA/guide fragments and keep Play links tied to one catalog.

No runtime rendering or framework is required. Run after editing the catalog;
--check verifies the committed static output without writing files.
"""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
CATALOG = json.loads((ROOT / 'content/acquisition.json').read_text())
APPS = CATALOG['apps']


def text(markup):
    return ' '.join(html.unescape(re.sub(r'<[^>]*>', '', markup)).split())


def attr(tag, name, value):
    escaped = html.escape(str(value), quote=True)
    pattern = rf'\s{re.escape(name)}="[^"]*"'
    if re.search(pattern, tag):
        return re.sub(pattern, f' {name}="{escaped}"', tag)
    return tag[:-1] + f' {name}="{escaped}">'


def render_cta(slug, location):
    spec = CATALOG['articles'][slug]
    app = APPS[spec['app']]
    ident = f"{spec['app']}-cta-{1 if location == 'mid' else 2}"
    title = spec['headline' if location == 'mid' else 'end_headline']
    description = spec['description' if location == 'mid' else 'end_description']
    campaign = spec.get('destination') == 'campaign'
    target = '/noctra/november-reset/' if campaign else app['play_url']
    label = 'Explore November Reset 2026' if campaign else f"Try {app['name']} on Google Play"
    event = 'november_reset_cta_click' if campaign else 'article_app_cta_click'
    external = '' if campaign else ' target="_blank" rel="noopener noreferrer"'
    benefits = ''.join(f'<li>{html.escape(b)}</li>' for b in spec['benefits']) if location == 'mid' else ''
    benefit_list = f'<ul class="app-cta-benefits">{benefits}</ul>' if benefits else ''
    return f'''<aside id="{ident}" class="app-cta" aria-labelledby="{ident}-heading" data-app="{spec['app']}" data-intent="{spec['intent']}">
  <span class="eyebrow">{app['name']} for Android</span>
  <h2 id="{ident}-heading">{html.escape(title)}</h2>
  <p>{html.escape(description)}</p>
  {benefit_list}
  <a class="btn primary" href="{target}" data-event="{event}" data-app="{spec['app']}" data-intent="{spec['intent']}" data-cta-location="{location}"{external}>{label}</a>
  <a class="app-cta-details" href="{app['path']}" data-event="article_product_click" data-app="{spec['app']}" data-cta-location="{location}">Explore {app['name']} features and permissions</a>
  <small class="app-cta-disclosure">NextFlow Apps develops {app['name']}. Free download; optional in-app purchases. {html.escape(spec['note'])}</small>
</aside>'''.replace('\n  \n', '\n\n')


def render_guides(app_key, campaign=False):
    choices = [slug for slug, spec in CATALOG['articles'].items() if spec['app'] == app_key]
    if campaign:
        choices.sort(key=lambda slug: CATALOG['articles'][slug].get('destination') != 'campaign')
    cards = []
    for slug in choices:
        source = (ROOT / 'articles' / slug / 'index.html').read_text()
        title = text(re.search(r'<h1\b[^>]*>(.*?)</h1>', source, re.S).group(1))
        cards.append(f'<li><a href="/articles/{slug}/">{html.escape(title)}</a></li>')
    app = APPS[app_key]
    return f'''<section id="related-guides" class="section product-guides" aria-labelledby="related-guides-heading">
  <div class="container"><div class="section-head"><h2 id="related-guides-heading">Useful guides for {app['name']}</h2><p>Start with a practical answer, whether or not you choose our app.</p></div>
  <ul class="guide-links">{''.join(cards)}</ul></div>
</section>'''


def render_plans(app_key):
    app = APPS[app_key]
    return f'''<section id="plans" class="section" aria-labelledby="plans-heading">
  <div class="container"><div class="section-head"><h2 id="plans-heading">Free to start. Premium when it fits.</h2><p>Android download with ads and optional in-app purchases. Check the app and Google Play purchase screen for current local prices and availability.</p></div>
  <div class="grid two"><div class="feature"><h3>Start free</h3><p>{html.escape(app['free'])}</p></div><div class="feature"><h3>Optional Premium</h3><p>{html.escape(app['premium'])}</p></div></div></div>
</section>'''


def render_proof(app_key):
    app = APPS[app_key]
    return f'''<section class="section product-proof" aria-labelledby="product-proof-heading">
  <div class="container"><div class="section-head"><h2 id="product-proof-heading">A look at {app['name']}</h2><p>A product visual from the official Google Play listing. The current interface and available features may vary by app version.</p></div>
  <figure class="store-visual"><img src="{app['screenshot']}" alt="{app['name']} product screenshot from its official Google Play listing" width="526" height="296" loading="lazy" decoding="async" /><figcaption><a href="{app['play_url']}" data-cta-location="product-visual" target="_blank" rel="noopener noreferrer">View {app['name']} on Google Play</a></figcaption></figure></div>
</section>'''


def replace_fragment(source, kind, content):
    pattern = rf'(<!-- nextflow:{kind} -->).*?(<!-- /nextflow:{kind} -->)'
    return re.sub(pattern, lambda m: m[1] + '\n' + content + '\n' + m[2], source, flags=re.S)


def sync_library(source):
    cards = [(url, text(title)) for url, title in re.findall(r'<h3>\s*<a href="(/articles/[^"#]+/)">(.*?)</a>\s*</h3>', source, re.S)]
    if len(cards) != len(CATALOG['articles']):
        raise ValueError('Article library must list every catalog guide once')
    description = html.unescape(re.search(r'<meta\s+name="description"\s+content="([^"]*)"', source)[1])
    for kind in ('property="og:description"', 'name="twitter:description"'):
        source = re.sub(rf'(<meta\s+{kind}\s+content=")[^"]*(")', lambda m: m[1] + html.escape(description, quote=True) + m[2], source)
    def schema(match):
        data = json.loads(match[2])
        if data.get('@type') != 'CollectionPage': return match[0]
        data['description'] = description
        data['mainEntity'] = {'@type': 'ItemList', 'numberOfItems': len(cards), 'itemListElement': [
            {'@type': 'ListItem', 'position': position, 'url': CATALOG['origin'] + url, 'name': title}
            for position, (url, title) in enumerate(cards, 1)]}
        return match[1] + '\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n' + match[3]
    return re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', schema, source, flags=re.S)


def normalize_links(source, relative):
    main_start, main_end = source.find('<main'), source.find('</main>')
    seen_play = 0
    article_slug = relative.split('/')[1] if relative.startswith('articles/') and relative != 'articles/index.html' else ''
    primary = CATALOG['articles'].get(article_slug, {}).get('app')

    def link(m):
        nonlocal seen_play
        tag = m[0]
        match = re.search(r'\bhref="([^"]*)"', tag)
        if not match:
            return tag
        url = urlsplit(html.unescape(match[1]))
        key = None
        if url.netloc == 'play.google.com':
            package = parse_qs(url.query).get('id', [''])[0]
            key = next((k for k, v in APPS.items() if v['package'] == package), None)
            if key is None:
                raise ValueError(f'{relative}: unknown Google Play package {package}')
            tag = attr(tag, 'href', APPS[key]['play_url'])
            location = re.search(r'data-cta-location="([^"]*)"', tag)
            old = re.search(r'data-event="([^"]*)"', tag)
            if location:
                location = location[1]
            elif old and old[1].startswith('nnn_'):
                location = old[1].rsplit('_', 1)[-1]
            else:
                location = 'hero' if seen_play == 0 and relative in [f'{k}/index.html' for k in APPS] else 'body'
            seen_play += 1
            event = 'article_app_cta_click' if article_slug else ('november_reset_cta_click' if relative == 'noctra/november-reset/index.html' else 'product_google_play_click')
            tag = attr(attr(tag, 'data-event', event), 'data-cta-location', location)
        elif main_start < m.start() < main_end:
            key = next((k for k, v in APPS.items() if url.path == v['path']), None)
            if primary and key == primary:
                tag = attr(tag, 'data-event', 'article_product_click')
            elif primary == 'noctra' and url.path == '/noctra/november-reset/':
                key = 'noctra'
                tag = attr(tag, 'data-event', 'november_reset_cta_click')
            elif url.path == '' and url.fragment == 'plans':
                key = relative.split('/')[0] if relative.split('/')[0] in APPS else None
                if key:
                    tag = attr(tag, 'data-event', 'pricing_interest_click')
        if key:
            tag = attr(tag, 'data-app', key)
            if 'data-event=' in tag and 'data-cta-location=' not in tag:
                tag = attr(tag, 'data-cta-location', 'body')
        return tag

    return re.sub(r'<a\b[^>]*>', link, source)


def sync(check=False):
    changed = []
    for path in sorted(ROOT.rglob('*.html')):
        if '.github' in path.parts or path.name.startswith('google'):
            continue
        relative = path.relative_to(ROOT).as_posix()
        source = path.read_text()
        updated = source
        if relative == 'articles/index.html':
            updated = sync_library(updated)
        if relative.startswith('articles/') and relative != 'articles/index.html':
            slug = relative.split('/')[1]
            if slug in CATALOG['articles']:
                for location in ('mid', 'end'):
                    updated = replace_fragment(updated, f'app-cta:{location}', render_cta(slug, location))
        key = relative.split('/')[0]
        if key in APPS and relative in (f'{key}/index.html', 'noctra/november-reset/index.html'):
            updated = replace_fragment(updated, 'product-guides', render_guides(key, 'november-reset' in relative))
            updated = replace_fragment(updated, 'product-plans', render_plans(key)) if key != 'noctra' else updated
            updated = replace_fragment(updated, 'product-proof', render_proof(key))
        updated = normalize_links(updated, relative)
        if updated != source:
            changed.append(relative)
            if not check:
                path.write_text(updated)
    if check and changed:
        raise SystemExit('Acquisition fragments/links need synchronization: ' + ', '.join(changed))
    print(f"{'PASS: catalog output is synchronized' if check else 'Synchronized'}; {len(changed)} changed pages")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    sync(parser.parse_args().check)
