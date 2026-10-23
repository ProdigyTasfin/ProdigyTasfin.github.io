/* Campaign UI only. Funnel measurement belongs to acquisition.js. */
(() => {
  const videoLink = document.querySelector('[data-video-load]');
  videoLink?.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    const frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/N845ulQnK0s?autoplay=1';
    frame.title = 'Noctra November Reset official campaign video';
    frame.allow = 'autoplay; encrypted-media; picture-in-picture';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    videoLink.replaceWith(frame);
    frame.focus();
  });
  const sticky = document.querySelector('.mobile-cta');
  const hero = document.querySelector('.campaign-hero');
  const footer = document.querySelector('.site-footer');
  if (!sticky || !hero || !('IntersectionObserver' in window)) return;
  let heroVisible = true;
  let footerVisible = false;
  const update = () => sticky.classList.toggle('visible', !heroVisible && !footerVisible && scrollY > 400);
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.target === hero) heroVisible = entry.isIntersecting;
      if (entry.target === footer) footerVisible = entry.isIntersecting;
    });
    update();
  });
  observer.observe(hero);
  if (footer) observer.observe(footer);
})();
