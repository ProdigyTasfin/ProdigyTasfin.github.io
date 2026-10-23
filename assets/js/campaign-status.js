/* Editorial dates only: Google Play determines actual prices and eligibility. */
(() => {
  const start = Date.parse('2026-11-01T00:00:00+06:00');
  const end = Date.parse('2026-12-01T00:00:00+06:00');
  let lastPhase;
  const update = () => {
    const now = Date.now();
    const phase = now < start ? 'upcoming' : now < end ? 'window' : 'ended';
    if (phase === lastPhase) return;
    lastPhase = phase;
    const copy = {
      upcoming: {
        status: 'Upcoming: November 1–30, 2026',
        notice: 'The proposed US$11.11 Lifetime price is planned for November 1–30 in eligible markets, subject to Google Play configuration. Noctra is free to download; confirm the final local offer before paying.',
        price: 'Planned US price',
        heading: 'A planned US$11.11 Lifetime offer.'
      },
      window: {
        status: 'November 2026 window · Check Google Play',
        notice: 'The scheduled November 1–30 campaign window is here. Check Google Play for the current offer, eligible market and final local price; the planned US$11.11 discount is not guaranteed by the date.',
        price: 'Planned price · Verify in Google Play',
        heading: 'Check the current Lifetime offer in Google Play.'
      },
      ended: {
        status: 'November 2026 campaign window ended',
        notice: 'The November 1–30, 2026 campaign window has ended. US$11.11 was the planned promotional price for eligible markets. Check Google Play for current plans and prices; do not assume the earlier offer still applies.',
        price: 'Historical planned US price',
        heading: 'November 2026 offer archive'
      }
    }[phase];
    document.querySelectorAll('[data-campaign-status]').forEach(el => { el.textContent = copy.status; });
    document.querySelectorAll('[data-campaign-notice]').forEach(el => { el.textContent = copy.notice; });
    document.querySelectorAll('[data-campaign-price-label]').forEach(el => { el.textContent = copy.price; });
    document.querySelectorAll('[data-campaign-offer-heading]').forEach(el => { el.textContent = copy.heading; });
    document.documentElement.dataset.campaignPhase = phase;
  };
  update();
  // Refresh a tab restored from sleep or the back/forward cache across a boundary.
  addEventListener('pageshow', update);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) update(); });
  setInterval(update, 60000);
})();
