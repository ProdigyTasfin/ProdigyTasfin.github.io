(() => {
  const emit = (name, detail = {}) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: name, ...detail });
    window.dispatchEvent(new CustomEvent('nextflow:analytics', { detail: { event: name, ...detail } }));
  };

  emit('nnn_landing_view', { page_path: window.location.pathname });

  const campaignParams = new URLSearchParams();
  const incoming = new URLSearchParams(window.location.search);
  incoming.forEach((value, key) => {
    if (key.toLowerCase().startsWith('utm_')) campaignParams.set(key, value);
  });

  document.querySelectorAll('.play-link').forEach((link) => {
    if ([...campaignParams].length) {
      const target = new URL(link.href);
      campaignParams.forEach((value, key) => target.searchParams.set(key, value));
      link.href = target.toString();
    }
    link.addEventListener('click', () => emit(link.dataset.event, { destination: 'google_play' }));
  });

  document.querySelectorAll('.tracked-link[data-event]').forEach((link) => {
    link.addEventListener('click', () => emit(link.dataset.event, { destination: 'youtube' }));
  });

  const seen = new Set();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const name = entry.target.dataset.viewEvent;
      if (entry.isIntersecting && !seen.has(name)) {
        seen.add(name);
        emit(name);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('[data-view-event]').forEach((section) => observer.observe(section));

  const sticky = document.querySelector('.mobile-cta');
  const hero = document.querySelector('.campaign-hero');
  if (sticky && hero) {
    new IntersectionObserver(([entry]) => sticky.classList.toggle('visible', !entry.isIntersecting), { threshold: 0.05 }).observe(hero);
  }
})();
