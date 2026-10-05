#!/usr/bin/env python3
"""Theme and premium browsing regressions, tested against real HTML pages."""
import functools
import os
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_): pass


def run():
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    pages = [p for p in ROOT.rglob('*.html') if '.github' not in p.parts and not p.name.startswith('google')]
    errors = []
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if os.environ.get('CHROMIUM_PATH'): options['executable_path'] = os.environ['CHROMIUM_PATH']
            b = p.chromium.launch(**options)
            for theme in ('light', 'dark'):
                ctx = b.new_context(color_scheme=theme, reduced_motion='reduce')
                ctx.route('https://**/*', lambda r: r.abort())
                q = ctx.new_page();q.on('pageerror', lambda e: errors.append(str(e)))
                for file in pages:
                    for width in (320, 900, 1440):
                        q.set_viewport_size({'width': width, 'height': 900})
                        q.goto(f'{origin}/{file.relative_to(ROOT).as_posix()}')
                        assert q.locator('html').get_attribute('data-theme') == theme, file
                        assert q.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{file}: {width}px {theme} overflow'
                        assert q.locator('.brand-mark img').first.get_attribute('src') == 'https://play-lh.googleusercontent.com/6WnXZqXM-VVJLyX_THGoTLeQNs9bMKT9j6-U01e1HbqCGkWukRmtyoFuRF9AQxxjdQ=s188-rw', 'Official brand logo must be preserved'
                        if width == 320:
                            q.locator('.menu-toggle').click()
                            assert q.locator('.nav-links').is_visible()
                            q.keyboard.press('Escape')
                            assert q.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'
                    print('PASS', theme, file.relative_to(ROOT), flush=True)
                ctx.close()
            ctx = b.new_context(color_scheme='dark', reduced_motion='reduce')
            ctx.route('https://**/*', lambda r: r.abort())
            q = ctx.new_page();q.on('pageerror', lambda e: errors.append(str(e)))
            q.goto(origin)
            q.locator('[data-theme-menu] summary').click()
            q.locator('[data-theme-choice][value="light"]').check()
            assert q.locator('html').get_attribute('data-theme') == 'light'
            q.goto(origin + '/articles/')
            assert q.locator('html').get_attribute('data-theme') == 'light', 'Theme did not persist across navigation'
            q.reload();assert q.locator('html').get_attribute('data-theme') == 'light'
            q.locator('[data-theme-menu] summary').click();q.locator('[data-theme-choice][value="system"]').check()
            assert q.locator('html').get_attribute('data-theme') == 'dark'
            q.emulate_media(color_scheme='light')
            q.wait_for_function("document.documentElement.dataset.theme === 'light'")
            assert q.locator('.article-card:visible').count() == 9
            assert q.locator('.article-card .article-cover').count() == 9
            q.locator('#article-search').fill('pomodoro');assert q.locator('.article-card:visible').count() == 2
            q.locator('#article-search').fill('')
            for topic, count in [('background audio', 2), ('focus & productivity', 2), ('digital wellbeing', 5), ('all', 9)]:
                q.locator(f'[data-topic="{topic}"]').click()
                assert q.locator('.article-card:visible').count() == count, topic
            card = q.locator('.article-card').first
            link = card.locator('h3 a').get_attribute('href')
            card.locator('.save-guide').click()
            q.locator('[data-topic="saved"]').click();assert q.locator('.article-card:visible').count() == 1
            q.reload();q.locator('[data-topic="saved"]').click();assert q.locator('.article-card:visible').count() == 1
            q.locator('.article-card:visible .save-guide').click()
            assert q.locator('.article-card:visible').count() == 0
            assert q.locator('[data-topic="saved"]').evaluate('(el)=>el===document.activeElement'), 'Removing the last saved guide must preserve keyboard focus'
            q.locator('[data-topic="all"]').click();q.locator('.article-card').first.locator('.save-guide').click()
            q.goto(origin + link)
            assert q.locator('.guide-tools .save-guide').get_attribute('aria-pressed') == 'true'
            q.locator('.guide-tools .save-guide').click()
            q.goto(origin + '/articles/');q.locator('[data-topic="saved"]').click()
            assert q.locator('.article-card:visible').count() == 0
            assert q.locator('[data-library-empty]').is_visible()
            q.locator('[data-library-reset]').click();assert q.locator('.article-card:visible').count() == 9
            q.locator('#article-search').fill('no-such-guide');assert q.locator('.article-card:visible').count() == 0
            q.goto(origin)
            for goal, app in [('listen', 'HushFlow'), ('protect', 'Noctra'), ('focus', 'Temvica')]:
                q.locator(f'[data-goal="{goal}"]').click()
                assert q.locator('[data-finder-app]').inner_text() == app
                assert q.locator(f'[data-goal="{goal}"]').get_attribute('aria-pressed') == 'true'
            q.goto(origin + '/articles/how-to-use-pomodoro-for-studying/')
            start = q.locator('.reading-progress span').evaluate('(el)=>getComputedStyle(el).transform')
            q.evaluate('scrollTo(0, 2000)');q.wait_for_timeout(50)
            assert q.locator('.reading-progress span').evaluate('(el)=>getComputedStyle(el).transform') != start
            assert q.locator('.table-of-contents [aria-current="location"]').count() == 1
            q.locator('.back-to-top').click();q.wait_for_timeout(50)
            assert q.evaluate('scrollY') == 0
            assert q.locator('h1').evaluate('(el)=>el===document.activeElement')
            q.locator('.guide-tools button').filter(has_text='Copy link').click()
            q.wait_for_timeout(100)
            assert q.locator('.guide-tool-status').inner_text(), 'Copy link must report success or explain fallback'
            ctx.close()
            # A browser that disallows storage still gets working theme, search, and saves for the visit.
            restricted = b.new_context(reduced_motion='reduce')
            restricted.route('https://**/*', lambda r:r.abort())
            restricted.add_init_script("Object.defineProperty(window, 'localStorage', {get(){throw new Error('Storage blocked')}})")
            q = restricted.new_page();q.on('pageerror', lambda e:errors.append(str(e)))
            q.goto(origin + '/articles/')
            q.locator('[data-theme-menu] summary').click();q.locator('[data-theme-choice][value="dark"]').check()
            assert q.locator('html').get_attribute('data-theme') == 'dark'
            q.locator('.article-card').first.locator('.save-guide').click();q.locator('[data-topic="saved"]').click()
            assert q.locator('.article-card:visible').count() == 1
            restricted.close()
            for scheme in ('light', 'dark'):
                native = b.new_context(java_script_enabled=False, color_scheme=scheme, viewport={'width':320,'height':900})
                native.route('https://**/*',lambda r:r.abort());q=native.new_page()
                q.goto(origin + '/articles/')
                assert q.locator('.article-card:visible').count() == 9
                assert q.locator('.nav-links').is_visible()
                assert not q.locator('[data-library-tools]').is_visible()
                expected = 'rgb(16, 25, 22)' if scheme=='dark' else 'rgb(247, 248, 245)'
                assert q.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor') == expected
                native.close()
            assert not errors, errors
            b.close();print('PASS: themes, persistence, system changes, filters, saved guides, finder, reading tools, blocked storage and no-JS fallback.')
    finally:
        server.shutdown();server.server_close()


if __name__ == '__main__': run()
