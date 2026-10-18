#!/usr/bin/env python3
"""Check Salvera discovery, existing design, native links and local image delivery."""
import functools
import os
import threading
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from check_ui import QuietHandler, ROOT


def run():
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    routes = ['/salvera/', '/salvera/privacy-policy.html', '/salvera/data-deletion.html', '/salvera/terms.html', '/salvera/support.html']
    errors, failed = [], []
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if os.environ.get('CHROMIUM_PATH'): options['executable_path'] = os.environ['CHROMIUM_PATH']
            browser = p.chromium.launch(**options)
            for theme in ('light', 'dark'):
                context = browser.new_context(color_scheme=theme, reduced_motion='reduce')
                context.route('https://**/*', lambda route: route.abort())
                q = context.new_page()
                q.on('pageerror', lambda e: errors.append(str(e)))
                q.on('response', lambda r: failed.append(f'{r.status}: {r.url}') if r.url.startswith(origin) and r.status >= 400 else None)
                for route in routes:
                    for width in (320, 390, 768, 1024, 1440):
                        q.set_viewport_size({'width':width,'height':900}); response = q.goto(origin + route)
                        assert response.status == 200, route
                        assert q.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route,width,theme)
                        assert q.locator('html').get_attribute('data-theme') == theme
                        assert q.locator('.nav-links a[href="/salvera/"]').count() == 1
                        assert q.locator('.site-footer nav[aria-label="Products"] a').count() == 4
                        assert 'Inter' in q.locator('body').evaluate('(el)=>getComputedStyle(el).fontFamily')
                        if route == '/salvera/' and width in (320,390):
                            assert q.locator('.hero .btn.primary').bounding_box()['y'] < 900, 'Salvera support action must be visible on mobile'
                        if width == 320:
                            q.locator('.menu-toggle').click(); assert q.locator('.nav-links').is_visible()
                            q.locator('.nav-links a[href="/salvera/"]').click(); assert q.url == origin+'/salvera/'
                            assert q.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'
                    q.goto(origin + route)
                    for image in q.locator('img[src^="/assets/salvera/"]').all():
                        image.scroll_into_view_if_needed()
                        q.wait_for_function('(src)=>{const image=[...document.images].find(i=>i.getAttribute("src")===src); return image?.complete && image.naturalWidth>0}', arg=image.get_attribute('src'))
                    assert q.locator('a[href*="play.google.com"]').count() == 0
                q.goto(origin)
                assert q.locator('.product-card').count() == 4
                q.locator('#product-salvera').scroll_into_view_if_needed()
                q.wait_for_function('()=>{const image=document.querySelector(".product-card:has(#product-salvera) img"); return image.complete && image.naturalWidth>0}')
                q.locator('.product-card').filter(has=q.locator('#product-salvera')).locator('.btn.primary').click()
                assert q.url == origin + '/salvera/'
                for route in routes:
                    q.locator(f'.product-subnav a[href="{route}"]').click()
                    assert q.url == origin + route
                    assert q.locator(f'.product-subnav a[href="{route}"]').get_attribute('aria-current') == 'page'
                q.goto(origin + '/salvera/data-deletion.html')
                request = q.locator('a.btn[href^="mailto:"]').first
                assert request.is_visible() and request.get_attribute('href').startswith('mailto:support@nextflow-apps.com?subject=Salvera%20account%20and%20data%20deletion%20request')
                assert q.locator('form').count() == 0
                context.close()
            native = browser.new_context(java_script_enabled=False, viewport={'width':320,'height':900})
            native.route('https://**/*', lambda route: route.abort()); q = native.new_page()
            for route in routes:
                q.goto(origin + route)
                assert q.locator('.nav-links').is_visible()
                assert q.locator('.product-subnav a').count() == 5
                assert q.evaluate('document.documentElement.scrollWidth <= innerWidth'), route
            assert not errors and not failed, (errors,failed)
            native.close(); browser.close()
            print('PASS: five Salvera pages at five widths in both themes, homepage discovery, four-product navigation, policy links, original local images, real mailto request and no-JS access.')
    finally:
        server.shutdown(); server.server_close()


if __name__ == '__main__': run()
