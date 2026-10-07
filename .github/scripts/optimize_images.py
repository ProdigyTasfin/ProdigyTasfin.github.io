#!/usr/bin/env python3
"""Create responsive WebP derivatives; preserve original artwork and image URLs.

Generation requires Pillow. --check only needs the Python standard library.
"""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = 'https://nextflow-apps.com'
MANIFEST = ROOT / 'assets/responsive/manifest.json'


def source_path(url, page):
    parsed = urlsplit(urljoin(ORIGIN + '/' + page.relative_to(ROOT).as_posix(), html.unescape(url)))
    return parsed.path if parsed.netloc == urlsplit(ORIGIN).netloc else None


def image_attr(tag, key, value):
    escaped = html.escape(str(value), quote=True)
    pattern = rf'\s{re.escape(key)}="[^"]*"'
    if re.search(pattern, tag):
        return re.sub(pattern, lambda _: f' {key}="{escaped}"', tag)
    suffix = ' />' if tag.endswith('/>') else '>'
    return tag.removesuffix('/>').removesuffix('>').rstrip() + f' {key}="{escaped}"' + suffix


def generate():
    from PIL import Image
    prior = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    reverse = {v['url']: key for key, item in prior.items() for v in item['variants']}
    pages = {p: p.read_text() for p in ROOT.rglob('*.html') if '.github' not in p.parts}
    originals = set()
    for page, source in pages.items():
        for match in re.finditer(r'<img\b[^>]*\bsrc="([^"]*)"[^>]*>', source):
            path = source_path(match[1], page)
            path = reverse.get(path, path)
            if path and path.endswith('.webp') and (ROOT / path.lstrip('/')).is_file():
                originals.add(path)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for url in sorted(originals):
        path = ROOT / url.lstrip('/')
        with Image.open(path) as original:
            original.load()
            largest = min(1440, original.width)
            widths = sorted({w for w in (480, 960, largest) if w <= largest})
            base = re.sub(r'[^a-z0-9-]', '-', str(path.relative_to(ROOT).with_suffix('')).lower()).strip('-')
            variants = []
            for width in widths:
                height = max(1, round(original.height * width / original.width))
                resized = original.resize((width, height), Image.Resampling.LANCZOS)
                target = MANIFEST.parent / f'{base}-{width}.webp'
                resized.save(target, 'WEBP', quality=86, method=6)
                variants.append({'url': '/' + target.relative_to(ROOT).as_posix(), 'width': width, 'height': height, 'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
            manifest[url] = {'source_bytes': path.stat().st_size, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'variants': variants}
    mapping = {key: item['variants'][-1] for key, item in manifest.items()}
    # Both original and previously rendered references resolve to the same source.
    for key, item in prior.items():
        if key in mapping:
            for variant in item['variants']:
                mapping[variant['url']] = mapping[key]
    for page, source in pages.items():
        def image(match):
            tag = match[0]
            found = re.search(r'\bsrc="([^"]*)"', tag)
            url = source_path(found[1], page)
            original_url = reverse.get(url, url)
            if original_url not in manifest:
                return tag
            variants = manifest[original_url]['variants']
            biggest = variants[-1]
            for key in ('src', 'width', 'height'):
                tag = image_attr(tag, key, biggest['url'] if key == 'src' else biggest[key])
            tag = image_attr(tag, 'srcset', ', '.join(f"{v['url']} {v['width']}w" for v in variants))
            is_card = page.relative_to(ROOT).as_posix() == 'articles/index.html'
            sizes = '(max-width: 640px) calc(100vw - 48px), (max-width: 1024px) calc((100vw - 80px) / 2), 360px' if is_card else '(max-width: 1024px) calc(100vw - 32px), 760px'
            tag = image_attr(tag, 'sizes', sizes)
            tag = image_attr(tag, 'loading', 'lazy')
            return tag
        updated = re.sub(r'<img\b[^>]*>', image, source)
        # Correct social-image and ImageObject dimensions without guessing ratios.
        for old, variant in mapping.items():
            updated = updated.replace(ORIGIN + old, ORIGIN + variant['url'])
        og = re.search(r'<meta\b[^>]*property="og:image"[^>]*content="([^"]*)"', updated)
        if og:
            selected = next((v for item in manifest.values() for v in item['variants'] if ORIGIN + v['url'] == og[1]), None)
            if selected:
                for prop in ('width', 'height'):
                    updated = re.sub(rf'(<meta\b[^>]*property="og:image:{prop}"[^>]*content=")[^"]*(")', lambda m: m[1] + str(selected[prop]) + m[2], updated)
        def ld(match):
            data = json.loads(match[2])
            def walk(value):
                if isinstance(value, list):
                    for item in value: walk(item)
                elif isinstance(value, dict):
                    if value.get('@type') == 'ImageObject':
                        selected = next((v for item in manifest.values() for v in item['variants'] if ORIGIN + v['url'] == value.get('url')), None)
                        if selected: value.update(width=selected['width'], height=selected['height'])
                    for item in value.values(): walk(item)
            walk(data)
            return match[1] + '\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n' + match[3]
        updated = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', ld, updated, flags=re.S)
        if updated != source: page.write_text(updated)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    baseline = sum(v['source_bytes'] for v in manifest.values())
    largest = sum(v['variants'][-1]['bytes'] for v in manifest.values())
    print(f'{len(manifest)} original images preserved; largest derivatives {baseline:,} -> {largest:,} bytes ({(1-largest/baseline)*100:.1f}% smaller)')


def check():
    data = json.loads(MANIFEST.read_text())
    for key, item in data.items():
        path = ROOT / key.lstrip('/')
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['source_sha256'], f'Regenerate changed source: {key}'
        for variant in item['variants']:
            derivative = ROOT / variant['url'].lstrip('/')
            assert derivative.stat().st_size == variant['bytes'], variant['url']
            assert hashlib.sha256(derivative.read_bytes()).hexdigest() == variant['sha256'], variant['url']
    print(f'PASS: responsive derivatives and source hashes for {len(data)} images')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    check() if parser.parse_args().check else generate()
