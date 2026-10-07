/* Campaign UI only. Funnel measurement belongs to acquisition.js. */
(() => {
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
