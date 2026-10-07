#!/usr/bin/env python3
"""Browser regression checks; external services are blocked for reproducibility."""
import functools
import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def run():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    pages = sorted(path for path in ROOT.rglob('*.html') if '.github' not in path.parts and not path.name.startswith('google') and 'http-equiv="refresh"' not in path.read_text())
    errors = []
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if os.environ.get('CHROMIUM_PATH'):
                options['executable_path'] = os.environ['CHROMIUM_PATH']
            browser = p.chromium.launch(**options)
            page = browser.new_page()
            page.route('https://**/*', lambda route: route.abort())
            page.on('pageerror', lambda error: errors.append(f'{page.url}: {error}'))
            for path in pages:
                relative = path.relative_to(ROOT).as_posix()
                for width in (320, 768, 1440):
                    page.set_viewport_size({'width': width, 'height': 900})
                    page.goto(f'{origin}/{relative}')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{relative}: overflow at {width}'
                    if width == 320:
                        toggle = page.locator('.menu-toggle')
                        if toggle.count() and toggle.is_visible():
                            toggle.click()
                            assert toggle.get_attribute('aria-expanded') == 'true', relative
                            assert page.locator('.nav-links').is_visible(), relative
                            page.keyboard.press('Escape')
                            assert toggle.get_attribute('aria-expanded') == 'false', relative
                            assert toggle.evaluate('(el) => el === document.activeElement'), relative
                            toggle.click()
                            page.mouse.click(5, 850)
                            assert toggle.get_attribute('aria-expanded') == 'false', relative
                    if width == 1440:
                        faq = page.locator('.faq details')
                        if faq.count():
                            summary = faq.first.locator('summary')
                            summary.click()
                            page.wait_for_timeout(300)
                            assert faq.first.evaluate('(el) => el.open'), relative
                            answer = faq.first.locator('.faq-answer').first
                            assert answer.evaluate('(el) => el.clientHeight > 20 && el.scrollHeight <= el.clientHeight + 1'), relative
                            summary.dispatch_event('click')
                            page.wait_for_timeout(40)
                            summary.dispatch_event('click')
                            page.wait_for_timeout(300)
                            assert faq.first.evaluate('(el) => el.open'), f'{relative}: interrupted FAQ toggle'
                            # Switching motion preferences during animation must settle cleanly.
                            summary.dispatch_event('click')
                            page.emulate_media(reduced_motion='reduce')
                            page.wait_for_timeout(50)
                            assert not faq.first.evaluate('(el) => el.open'), relative
                            summary.click()
                            assert faq.first.evaluate('(el) => el.open'), relative
                            page.emulate_media(reduced_motion='no-preference')
                print('PASS layouts and interactions:', relative, flush=True)
            assert not errors, '\n'.join(errors)
            # Content and navigation remain available if scripts are blocked or disabled.
            context = browser.new_context(java_script_enabled=False, viewport={'width': 320, 'height': 900})
            native = context.new_page()
            native.route('https://**/*', lambda route: route.abort())
            for path in pages:
                relative = path.relative_to(ROOT).as_posix()
                native.goto(f'{origin}/{relative}')
                assert native.locator('.nav-links').is_visible(), f'{relative}: no-JS navigation missing'
                assert native.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{relative}: no-JS overflow'
                faq = native.locator('main details:not(.table-of-contents)')
                if faq.count():
                    faq.first.locator('summary').click()
                    assert faq.first.evaluate('(el) => el.open'), relative
                    assert faq.first.locator('p').first.is_visible(), relative
            context.close()
            # Policy dates must never be changed to the visitor's current date.
            for relative, date in [('privacy-policy.html', 'October 7, 2026'), ('refund-policy.html', 'August 2026'), ('hushflow/privacy-policy.html', 'July 2026')]:
                page.goto(f'{origin}/{relative}')
                assert date in page.locator('.last-updated').inner_text(), relative
            page.goto(f'{origin}/articles/how-to-use-pomodoro-for-studying/')
            page.emulate_media(reduced_motion='reduce')
            if not page.locator('.table-of-contents').evaluate('(el)=>el.open'):
                page.locator('.table-of-contents summary').click()
            link = page.locator('.table-of-contents a').first
            target = link.get_attribute('href')
            link.click()
            assert page.url.endswith(target), 'Native contents navigation must update the URL'
            assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto'
            page.set_viewport_size({'width': 320, 'height': 900})
            page.goto(f'{origin}/noctra/november-reset/')
            assert not page.locator('.mobile-cta').is_visible(), 'Offscreen CTA must not receive focus'
            page.evaluate("window.scrollTo(0, document.querySelector('.campaign-hero').offsetTop + document.querySelector('.campaign-hero').offsetHeight + 40)")
            page.wait_for_timeout(300)
            assert page.locator('.mobile-cta').is_visible()
            page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            page.wait_for_timeout(300)
            assert not page.locator('.mobile-cta').is_visible(), 'CTA must hide when the footer is visible'
            assert not errors, '\n'.join(errors)
            browser.close()
            print(f'PASS: {len(pages)} pages at three widths; native navigation/FAQ, policy dates, reduced motion, campaign CTA and no JS errors.')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    run()
