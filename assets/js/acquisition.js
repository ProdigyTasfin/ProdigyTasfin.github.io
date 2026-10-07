/* Local, minimal funnel events. No collector or network request is enabled here. */
(() => {
  if (window.NextFlowAnalytics) return;
  const events = [];
  const validNames = new Set(['acquisition_page_view', 'app_cta_view', 'article_app_cta_click', 'article_product_click', 'product_google_play_click', 'pricing_interest_click', 'november_reset_cta_click']);
  const appKeys = new Set(['hushflow', 'noctra', 'temvica']);
  const canonical = document.querySelector('link[rel="canonical"]')?.href;
  const pagePath = canonical ? new URL(canonical).pathname : null;
  const pageType = document.body.classList.contains('page-guide') ? 'article' : document.body.classList.contains('page-campaign') ? 'campaign' : document.body.classList.contains('page-product') ? 'product' : 'other';
  const slug = pageType === 'article' ? pagePath?.split('/')[2] : '';
  let consent = false;
  let adapter = null;
  const permitted = () => consent && navigator.doNotTrack !== '1' && !navigator.globalPrivacyControl;
  const record = (name, detail = {}) => {
    if (!pagePath || !validNames.has(name)) return;
    const event = Object.freeze({ event: name, source_page: pagePath, page_type: pageType,
      ...(appKeys.has(detail.app) ? { app: detail.app } : {}),
      ...(slug ? { article_slug: slug } : {}),
      ...(detail.cta_location ? { cta_location: String(detail.cta_location).slice(0, 40) } : {}),
      ...(validNames.has(detail.cta_action) ? { cta_action: detail.cta_action } : {}),
      ...(detail.destination === 'google_play' || detail.destination === 'product' || detail.destination === 'campaign' ? { destination: detail.destination } : {}) });
    events.push(event); if (events.length > 100) events.shift();
    window.dispatchEvent(new CustomEvent('nextflow:analytics', { detail: event }));
    if (permitted() && adapter) { try { adapter(event); } catch (_) { /* Measurement must never block navigation. */ } }
  };
  window.NextFlowAnalytics = Object.freeze({
    record,
    getEvents: () => events.map((event) => ({ ...event })),
    setConsent: (value) => { consent = value === true; },
    setAdapter: (callback) => { adapter = typeof callback === 'function' ? callback : null; }
  });
  // A consent/collector integration can attach before the first measured event.
  window.dispatchEvent(new CustomEvent('nextflow:analytics-ready'));
  // Keep a useful denominator once per page, without a visitor/session identifier.
  record('acquisition_page_view');
  const clicked = new WeakSet();
  document.addEventListener('click', (event) => {
    const link = event.target.closest?.('a[data-event][data-app]');
    if (!link || event.defaultPrevented || clicked.has(link)) return;
    clicked.add(link);
    const target = new URL(link.href, location.href);
    record(link.dataset.event, { app: link.dataset.app, cta_location: link.dataset.ctaLocation || 'body',
      destination: target.hostname === 'play.google.com' ? 'google_play' : target.pathname === '/noctra/november-reset/' ? 'campaign' : 'product' });
  });
  // Auxclick covers opening the same links with the mouse's middle button.
  document.addEventListener('auxclick', (event) => {
    if (event.button !== 1) return;
    const link = event.target.closest?.('a[data-event][data-app]');
    if (!link || clicked.has(link)) return;
    clicked.add(link);
    const target = new URL(link.href, location.href);
    record(link.dataset.event, { app: link.dataset.app, cta_location: link.dataset.ctaLocation || 'body',
      destination: target.hostname === 'play.google.com' ? 'google_play' : target.pathname === '/noctra/november-reset/' ? 'campaign' : 'product' });
  });
  if ('IntersectionObserver' in window) {
    const seen = new WeakSet();
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (!entry.isIntersecting || entry.intersectionRatio < 0.5 || seen.has(entry.target)) return;
      seen.add(entry.target); observer.unobserve(entry.target);
      record('app_cta_view', { app: entry.target.dataset.app, cta_location: entry.target.dataset.ctaLocation || 'body', cta_action: entry.target.dataset.event });
    }), { threshold: 0.5 });
    document.querySelectorAll('a[data-event][data-app]').forEach((link) => observer.observe(link));
  }
})();
