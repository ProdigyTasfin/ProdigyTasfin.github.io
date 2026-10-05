/* Shared navigation. The links remain available when JavaScript is disabled. */
(() => {
  const toggle = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');

  if (toggle && links) {
    document.documentElement.classList.add('nav-enhanced');
    const setOpen = (open) => {
      links.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
      toggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
    };
    setOpen(false);
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    links.addEventListener('click', (event) => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', (event) => {
      if (!links.contains(event.target) && !toggle.contains(event.target)) setOpen(false);
    });
    document.addEventListener('focusin', (event) => {
      if (!links.contains(event.target) && !toggle.contains(event.target)) setOpen(false);
    });
    // Resizing back to mobile must not revive an old open menu.
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(() => {
        if (getComputedStyle(toggle).display === 'none') setOpen(false);
      });
      observer.observe(toggle);
    }
  }
  // Copyright years can be current; policy revision dates stay authored in HTML.
  document.querySelectorAll('[data-year]').forEach((element) => {
    element.textContent = new Date().getFullYear();
  });
})();
