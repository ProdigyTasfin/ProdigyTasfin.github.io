#!/usr/bin/env python3
"""Validate the four-product portfolio, Salvera routes and official PNG provenance."""
import hashlib
import json
import re
import struct
from urllib.parse import unquote, urlsplit
from check_site import ROOT, Page, ORIGIN
from check_acquisition import nodes


def png_size(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    return struct.unpack('>II', data[16:24])


def run():
    products = json.loads((ROOT / 'content/products.json').read_text())['products']
    assert [p['key'] for p in products] == ['hushflow', 'noctra', 'temvica', 'salvera']
    rendered = 0
    for path in ROOT.rglob('*.html'):
        if '.git' in path.parts or '.github' in path.parts: continue
        source = path.read_text()
        primary = re.search(r'<nav\b[^>]*class="nav-links"[^>]*>.*?</nav>', source, re.S)
        if not primary: continue
        rendered += 1
        assert primary[0].count('href="/salvera/"') == 1, f'{path}: Salvera primary navigation'
        footer = re.search(r'<nav\b[^>]*class="footer-col"[^>]*aria-label="Products"[^>]*>.*?</nav>', source, re.S)
        assert footer, path
        for product in products:
            assert footer[0].count(f'href="{product["path"]}"') == 1, f'{path}: product footer'
        assert '6WnXZqXM-VVJLyX_THGoTLeQNs9bMKT9j6-U01e1HbqCGkWukRmtyoFuRF9AQxxjdQ=s188-rw' in source, path
        assert 'support@nextflow-apps.com' in source, path
    manifest = json.loads((ROOT / 'assets/salvera/manifest.json').read_text())
    original = ROOT / manifest['source'].lstrip('/')
    copied = ROOT / manifest['original_copy'].lstrip('/')
    assert original.read_bytes() == copied.read_bytes(), 'Original Salvera logo must be copied exactly'
    assert hashlib.sha256(original.read_bytes()).hexdigest() == manifest['source_sha256']
    assert png_size(original) == (manifest['width'], manifest['height'])
    for variant in manifest['variants']:
        path = ROOT / variant['path'].lstrip('/')
        assert png_size(path) == (variant['width'], variant['height'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == variant['sha256'], path
        assert variant['width'] * manifest['height'] == variant['height'] * manifest['width']
    home = Page((ROOT / 'index.html').read_text())
    graph = [node for a, body in home.scripts if a.get('type') == 'application/ld+json' for node in nodes(json.loads(body))]
    listing = next(node for node in graph if node.get('@type') == 'ItemList')
    assert listing['numberOfItems'] == 4
    assert [(i['position'], i['name'], i['url']) for i in listing['itemListElement']] == [(i, p['name'], ORIGIN+p['path']) for i,p in enumerate(products,1)]
    assert 'id="product-salvera"' in (ROOT / 'index.html').read_text()
    routes = ['/salvera/', '/salvera/privacy-policy.html', '/salvera/terms.html', '/salvera/support.html', '/salvera/data-deletion.html']
    for route in routes:
        path = ROOT / route.lstrip('/')
        if path.is_dir(): path /= 'index.html'
        source = path.read_text(); page = Page(source)
        assert page.canonicals == [ORIGIN+route], path
        assert page.metadata['robots'] == 'index, follow', path
        assert page.metadata['og:image'] == ORIGIN+'/assets/salvera/logo-384.png', path
        for other in routes: assert other in page.references, f'{path}: missing local Salvera navigation {other}'
        assert '/assets/salvera/logo-32.png' in page.references and '/assets/salvera/logo-180.png' in page.references, path
        assert not re.search(r'<form\b', source), 'No pretend account/deletion form'
        for ref in page.references:
            assert urlsplit(ref).netloc != 'play.google.com', 'Do not invent a Salvera Play listing'
        graph = [node for a, body in page.scripts if a.get('type') == 'application/ld+json' for node in nodes(json.loads(body))]
        for node in graph:
            assert not any(field in node for field in ('aggregateRating', 'ratingValue', 'review', 'downloadUrl', 'offers', 'softwareVersion')), path
    deletion = Page((ROOT / 'salvera/data-deletion.html').read_text())
    requests = [ref for ref in deletion.references if ref.startswith('mailto:') and 'deletion%20request' in ref]
    assert requests and all(urlsplit(ref).path == 'support@nextflow-apps.com' for ref in requests)
    assert 'Salvera account and data deletion request' in unquote(requests[0])
    print(f'PASS: {rendered} consistent product headers/footers, four-product schema, five Salvera routes, real mailto deletion request and exact official PNG provenance.')


if __name__ == '__main__': run()
