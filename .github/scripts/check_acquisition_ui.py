#!/usr/bin/env python3
"""Exercise real acquisition navigation and the consent-gated measurement contract."""
import functools
import json
import os
import threading
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
from check_ui import QuietHandler, ROOT


class PagesHandler(QuietHandler):
    def send_error(self, code, message=None, explain=None):
        if code != 404: return super().send_error(code, message, explain)
        content = (ROOT / '404.html').read_bytes()
        self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content))); self.end_headers()
        if self.command != 'HEAD': self.wfile.write(content)


def run():
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(PagesHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    catalog = json.loads((ROOT / 'content/acquisition.json').read_text())
    aliases = json.loads((ROOT / 'content/redirects.json').read_text())
    errors = []
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if os.environ.get('CHROMIUM_PATH'): options['executable_path'] = os.environ['CHROMIUM_PATH']
            browser = p.chromium.launch(**options)
            context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
            context.route('https://**/*', lambda route: route.abort())
            page = context.new_page(); page.on('pageerror', lambda error: errors.append(str(error)))
            for slug, spec in catalog['articles'].items():
                page.goto(origin + f'/articles/{slug}/?email=private@example.test&utm_source=private')
                assert page.locator('.app-cta').count() == 2
                assert page.locator('.app-cta .btn.primary').count() == 2
                assert not page.locator('.table-of-contents').evaluate('(el)=>el.open'), slug
                if spec['app'] == 'hushflow':
                    assert page.locator('.article-content > section').first.bounding_box()['y'] < 844, f'{slug}: answer below mobile viewport'
                assert all(key == spec['app'] for key in page.locator('.app-cta').evaluate_all('(els)=>els.map(el=>el.dataset.app)'))
                cta = page.locator('.app-cta .btn.primary').first
                cta.scroll_into_view_if_needed()
                assert cta.bounding_box()['height'] >= 44
                page.wait_for_function("NextFlowAnalytics.getEvents().some(e=>e.event==='app_cta_view' && e.cta_location==='mid' && (e.cta_action==='article_app_cta_click' || e.cta_action==='november_reset_cta_click'))")
                # Actual outbound action opens Play without the tracking listener cancelling it.
                if spec.get('destination') != 'campaign':
                    with page.expect_popup() as popup_info: cta.click()
                    popup_info.value.close()
                else:
                    page.evaluate("window.addEventListener('nextflow:analytics', e=>sessionStorage.setItem('test-last-event', JSON.stringify(e.detail)))")
                    cta.click()
                    assert page.url == origin + '/noctra/november-reset/'
                events = [json.loads(page.evaluate("sessionStorage.getItem('test-last-event')"))] if spec.get('destination') == 'campaign' else page.evaluate('NextFlowAnalytics.getEvents()')
                name = 'november_reset_cta_click' if spec.get('destination') == 'campaign' else 'article_app_cta_click'
                clicks = [e for e in events if e['event'] == name and e.get('cta_location') == 'mid']
                assert len(clicks) == 1 and clicks[0]['app'] == spec['app'], slug
                assert clicks[0]['source_page'] == f'/articles/{slug}/' and clicks[0]['article_slug'] == slug
                assert 'private' not in json.dumps(events) and '@' not in json.dumps(events)
                # A duplicate observer/auxiliary click must not create another event for this anchor.
                if spec.get('destination') != 'campaign':
                    cta.dispatch_event('auxclick', {'button': 1})
                    assert len([e for e in page.evaluate('NextFlowAnalytics.getEvents()') if e['event'] == name and e.get('cta_location') == 'mid']) == 1
            for key in catalog['apps']:
                page.goto(origin + f'/{key}/')
                hero = page.locator('a[data-event="product_google_play_click"][data-cta-location="hero"]').first
                assert hero.is_visible() and hero.bounding_box()['y'] < 844, f'{key}: Play CTA below mobile viewport'
                with page.expect_popup() as popup_info: hero.click()
                popup_info.value.close()
                assert any(e['event'] == 'product_google_play_click' and e['cta_location'] == 'hero' and e['app'] == key for e in page.evaluate('NextFlowAnalytics.getEvents()'))
                pricing = page.locator('a[data-event="pricing_interest_click"]').first
                pricing.click(); assert page.url.endswith('#plans')
                assert any(e['event'] == 'pricing_interest_click' for e in page.evaluate('NextFlowAnalytics.getEvents()'))
            # No integration is active by default; installing an adapter alone is insufficient.
            page.goto(origin + '/hushflow/')
            page.evaluate("window.sent=[]; NextFlowAnalytics.setAdapter(e=>sent.push(e)); NextFlowAnalytics.record('product_google_play_click',{app:'hushflow',email:'private'});")
            assert page.evaluate('sent.length') == 0
            page.evaluate("NextFlowAnalytics.setConsent(true); NextFlowAnalytics.record('product_google_play_click',{app:'hushflow'});")
            assert page.evaluate('sent.length') == 1, 'Opt-in must enable only future events'
            page.evaluate("NextFlowAnalytics.setConsent(false); NextFlowAnalytics.record('product_google_play_click',{app:'hushflow'});")
            assert page.evaluate('sent.length') == 1, 'Revocation must stop forwarding'
            page.evaluate("NextFlowAnalytics.setConsent(true); NextFlowAnalytics.setAdapter(()=>{throw Error('Collector failed')}); NextFlowAnalytics.record('product_google_play_click'); for(let i=0;i<150;i++)NextFlowAnalytics.record('acquisition_page_view');")
            assert page.evaluate('NextFlowAnalytics.getEvents().length') == 100
            assert not errors, errors
            for flag in ('doNotTrack', 'globalPrivacyControl'):
                private = browser.new_context()
                private.route('https://**/*', lambda route: route.abort())
                value = "'1'" if flag == 'doNotTrack' else 'true'
                private.add_init_script(f"Object.defineProperty(navigator, '{flag}', {{get:()=>{value}}});")
                q = private.new_page(); q.goto(origin + '/noctra/')
                q.evaluate("window.sent=[]; NextFlowAnalytics.setAdapter(e=>sent.push(e)); NextFlowAnalytics.setConsent(true); NextFlowAnalytics.record('product_google_play_click',{app:'noctra'});")
                assert q.evaluate('sent.length') == 0, flag
                private.close()
            # Redirects also work without JavaScript. Rewrite only the canonical host for local testing.
            native = browser.new_context(java_script_enabled=False, viewport={'width':320,'height':900})
            native.route('https://**/*', lambda route: route.abort())
            native.route('https://nextflow-apps.com/**', lambda route: route.fulfill(status=302, headers={'location':origin + urlsplit(route.request.url).path}))
            q = native.new_page()
            for alias, target in aliases.items():
                q.goto(origin + alias, wait_until='domcontentloaded')
                q.wait_for_url(origin + target)
                assert q.locator('h1').inner_text() == 'How to Play Music With the Screen Off on Android'
            response = q.goto(origin + '/missing/nested/path/')
            assert response.status == 404 and q.locator('meta[name="robots"]').get_attribute('content') == 'noindex, follow'
            assert q.locator('link[rel="canonical"]').count() == 0
            q.locator('main a').filter(has_text='Browse the guides').click()
            assert q.url == origin + '/articles/' and q.locator('.article-card:visible').count() == 9
            q.goto(origin + '/articles/how-to-play-audio-with-screen-off-android/')
            assert q.locator('.app-cta .btn.primary').count() == 2
            native.close(); context.close(); browser.close()
            print('PASS: nine contextual funnels, mobile product Play/pricing actions, no-JS aliases and 404 recovery; consent, revocation, DNT/GPC, duplicate suppression and no query/PII forwarding.')
    finally:
        server.shutdown(); server.server_close()


if __name__ == '__main__': run()
