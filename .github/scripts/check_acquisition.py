#!/usr/bin/env python3
"""Check content/schema alignment, app relationships and crawlable acquisition paths."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from check_site import Page, ROOT, ORIGIN, page_url
from sync_acquisition import text


class Content(Page):
    def __init__(self, source):
        self.elements, self.words, self.captures = [], {}, []
        super().__init__(source)

    def handle_starttag(self, tag, attributes):
        super().handle_starttag(tag, attributes)
        a = dict(attributes)
        self.elements.append((tag, a))
        if tag == 'br':
            for _, _, parts in self.captures: parts.append(' ')
        if tag in ('h1', 'title', 'time'):
            self.captures.append((tag, a, []))

    def handle_data(self, data):
        super().handle_data(data)
        for _, _, parts in self.captures:
            parts.append(data)

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        for index, (key, a, parts) in enumerate(self.captures):
            if key == tag:
                self.words.setdefault(tag, []).append((a, ' '.join(''.join(parts).split())))
                self.captures.pop(index)
                break


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def run():
    catalog = json.loads((ROOT / 'content/acquisition.json').read_text())
    manifest = json.loads((ROOT / 'assets/responsive/manifest.json').read_text())
    variants = {ORIGIN + variant['url']: variant for item in manifest.values() for variant in item['variants']}
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    modifications = {entry.find('s:loc', ns).text: entry.findtext('s:lastmod', namespaces=ns) for entry in sitemap.findall('s:url', ns)}
    titles, descriptions, article_count, play_count = set(), set(), 0, 0
    for url in modifications:
        path = ROOT / url.removeprefix(ORIGIN).lstrip('/')
        if path.is_dir(): path /= 'index.html'
        source = path.read_text()
        page = Content(source)
        title = page.words['title'][0][1]
        description = page.metadata['description']
        assert title not in titles, f'Duplicate title: {path}'
        assert description not in descriptions, f'Duplicate description: {path}'
        titles.add(title); descriptions.add(description)
        if url.endswith('/'):
            assert page.metadata.get('og:title'), f'Missing Open Graph title: {path}'
            assert page.metadata.get('og:description'), f'Missing Open Graph description: {path}'
        assert sum(a.get('src') == '/assets/js/acquisition.js' for a, _ in page.scripts) == 1, path
        for tag, a in page.elements:
            if tag == 'a' and urlsplit(a.get('href', '')).netloc == 'play.google.com':
                key = a.get('data-app')
                assert key in catalog['apps'] and a['href'] == catalog['apps'][key]['play_url'], path
                assert a.get('data-event') and a.get('data-cta-location'), path
                play_count += 1
            if tag == 'img' and a.get('src', '').startswith('/assets/responsive/'):
                selected = variants[ORIGIN + a['src']]
                assert (int(a['width']), int(a['height'])) == (selected['width'], selected['height']), path
                assert a.get('sizes') and a.get('srcset') and a.get('loading') == 'lazy', path
                for url_width in a['srcset'].split(','):
                    asset, width = url_width.strip().split()
                    assert variants[ORIGIN + asset]['width'] == int(width[:-1]), path
        graph = [item for a, body in page.scripts if a.get('type') == 'application/ld+json' for item in nodes(json.loads(body))]
        assert not any(item.get('@type') == 'FAQPage' for item in graph), path
        for item in graph:
            if item.get('@type') == 'ImageObject' and item.get('url') in variants:
                v = variants[item['url']]
                assert item.get('width') == v['width'] and item.get('height') == v['height'], path
            if item.get('@type') in ('MobileApplication', 'SoftwareApplication'):
                assert not any(field in item for field in ('review', 'aggregateRating', 'interactionStatistic')), path
                assert item.get('operatingSystem') == 'Android', path
        relative = path.relative_to(ROOT).as_posix()
        if relative == 'articles/index.html':
            visible = [(ORIGIN + route, text(label)) for route, label in re.findall(r'<h3>\s*<a href="(/articles/[^"#]+/)">(.*?)</a>\s*</h3>', source, re.S)]
            listing = next(item for item in graph if item.get('@type') == 'ItemList')
            assert listing['numberOfItems'] == len(visible) == 9
            assert [(item['url'], item['name']) for item in listing['itemListElement']] == visible
            assert [item['position'] for item in listing['itemListElement']] == list(range(1, 10))
        if relative.startswith('articles/') and relative != 'articles/index.html':
            slug = relative.split('/')[1]; spec = catalog['articles'][slug]
            article_count += 1
            articles = [item for item in graph if item.get('@type') in ('Article', 'BlogPosting')]
            assert len(articles) == 1, path
            article = articles[0]
            assert article['headline'] == page.words['h1'][0][1], f'Headline drift: {path}'
            assert article['description'] == description, f'Article description drift: {path}'
            dates = {a.get('datetime') for a, _ in page.words.get('time', [])}
            assert article['datePublished'] in dates and article['dateModified'] in dates, path
            assert modifications[url] == article['dateModified'], path
            assert article['datePublished'] <= article['dateModified'], path
            ctas = [a for tag, a in page.elements if tag == 'aside' and 'app-cta' in a.get('class', '').split()]
            assert len(ctas) == 2 and all(a['data-app'] == spec['app'] for a in ctas), path
            assert source.index('class="app-cta"') > source.index(f'id="{spec["insert_after"]}"'), path
            assert 'NextFlow Apps develops' in source, path
            # Preserve an answer before artwork and the first recommendation.
            hero = re.search(r'<figure\b[^>]*class="article-hero"', source)
            intro = re.search(r'<section\b[^>]*id="(?:introduction|direct-answer)"', source)
            if hero and intro: assert hero.start() > intro.start(), path
    assert article_count == len(catalog['articles']) == 9
    for key, app in catalog['apps'].items():
        page = Content((ROOT / key / 'index.html').read_text())
        for slug, spec in catalog['articles'].items():
            if spec['app'] == key:
                assert f'/articles/{slug}/' in page.references, f'Missing product -> guide: {key}, {slug}'
        assert 'plans' in page.ids and 'related-guides' in page.ids, key
    winner = Content((ROOT / 'articles/how-to-play-audio-with-screen-off-android/index.html').read_text())
    assert winner.words['title'][0][1] == 'How to Play Music With the Screen Off on Android'
    assert winner.canonicals == [ORIGIN + '/articles/how-to-play-audio-with-screen-off-android/']
    assert 'screen-off-vs-powered-off' in winner.ids
    print(f'PASS: {len(modifications)} unique titles/descriptions, {article_count} intent-matched guides, {play_count} canonical Play links, truthful schema and responsive images.')


if __name__ == '__main__': run()
