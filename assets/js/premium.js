/* Appearance and browsing enhancements. No accounts or remote storage required. */
(() => {
  const root = document.documentElement;
  const icon = (path, size = 18) => {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const shape = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('width', String(size)); svg.setAttribute('height', String(size));
    svg.setAttribute('fill', 'none'); svg.setAttribute('stroke', 'currentColor'); svg.setAttribute('stroke-width', '1.7');
    svg.setAttribute('stroke-linecap', 'round'); svg.setAttribute('stroke-linejoin', 'round'); svg.setAttribute('aria-hidden', 'true');
    shape.setAttribute('d', path); svg.append(shape); return svg;
  };
  const outwardArrow = 'M6 18 18 6M6 6h12v12';
  const scheme = matchMedia('(prefers-color-scheme: dark)');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let storageAvailable = true;
  const read = (key) => { try { return localStorage.getItem(key); } catch (_) { storageAvailable = false; return null; } };
  const write = (key, value) => { try { localStorage.setItem(key, value); return true; } catch (_) { storageAvailable = false; return false; } };
  let preference = read('nextflow-theme') || 'system';
  if (!['light', 'dark', 'system'].includes(preference)) preference = 'system';
  const applyTheme = () => {
    const theme = preference === 'system' ? (scheme.matches ? 'dark' : 'light') : preference;
    root.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#101916' : '#f7f8f5');
    document.querySelectorAll('[data-theme-choice]').forEach((input) => { input.checked = input.value === preference; });
  };
  applyTheme();
  scheme.addEventListener('change', () => { if (preference === 'system') applyTheme(); });
  const themeMenu = document.querySelector('[data-theme-menu]');
  if (themeMenu) {
    themeMenu.hidden = false;
    themeMenu.addEventListener('change', (event) => {
      if (!event.target.matches('[data-theme-choice]')) return;
      preference = event.target.value;
      if (!write('nextflow-theme', preference) && !themeMenu.querySelector('small')) {
        const note = document.createElement('small'); note.textContent = 'For this visit only; browser storage is unavailable.'; themeMenu.querySelector('fieldset').append(note);
      }
      applyTheme();
    });
    document.addEventListener('click', (event) => { if (!themeMenu.contains(event.target)) themeMenu.open = false; });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && themeMenu.open) { themeMenu.open = false; themeMenu.querySelector('summary').focus(); }
    });
  }

  let saved = new Set();
  const parseSaved = (raw) => {
    try {
      const values = JSON.parse(raw || '[]');
      return new Set(Array.isArray(values) ? values.filter((value) => typeof value === 'string' && value.startsWith('/articles/')) : []);
    } catch (_) { return new Set(); }
  };
  saved = parseSaved(read('nextflow-saved-guides'));
  const saveButtons = [];
  const syncSaves = () => {
    saveButtons.forEach(({ button, url, title }) => {
      const active = saved.has(url);
      button.setAttribute('aria-pressed', String(active));
      button.textContent = active ? 'Saved guide' : 'Save guide';
      button.setAttribute('aria-label', active ? `Saved guide: ${title}. Activate to remove.` : `Save guide: ${title}`);
    });
  };
  const makeSaveButton = (url, title, status) => {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'save-guide';
    button.setAttribute('aria-label', `Save guide: ${title}`);
    saveButtons.push({ button, url, title });
    button.addEventListener('click', () => {
      if (saved.has(url)) saved.delete(url); else saved.add(url);
      const persisted = write('nextflow-saved-guides', JSON.stringify([...saved]));
      syncSaves();
      if (status) status.textContent = saved.has(url) ? (persisted ? 'Saved on this device.' : 'Saved for this visit; browser storage is unavailable.') : 'Removed from saved guides.';
      filterLibrary();
      if (button.closest('.article-card')?.hidden) {
        const next = cards.find((card) => !card.hidden)?.querySelector('.save-guide');
        (next || document.querySelector('[data-topic="saved"]')).focus();
      }
    });
    return button;
  };

  const cards = [...document.querySelectorAll('.page-library .article-card')];
  const search = document.querySelector('#article-search');
  const libraryCount = document.querySelector('[data-library-count]');
  let topic = 'all';
  function filterLibrary() {
    if (!cards.length) return;
    const query = (search?.value || '').trim().toLocaleLowerCase();
    let count = 0;
    cards.forEach((card) => {
      const url = card.querySelector('h3 a').getAttribute('href');
      const category = card.dataset.articleCategory;
      const text = `${card.querySelector('h3').textContent} ${card.querySelector('p').textContent} ${category}`.toLocaleLowerCase();
      const show = (topic === 'all' || (topic === 'saved' ? saved.has(url) : category === topic || card.dataset.articleSeason === topic)) && text.includes(query);
      card.hidden = !show;
      if (show) { count++; card.classList.remove('reveal-pending'); }
    });
    libraryCount.textContent = `${count} ${count === 1 ? 'guide' : 'guides'}${topic === 'saved' ? (storageAvailable ? ' saved on this device' : ' saved for this visit') : ' to explore'}`;
    document.querySelector('[data-library-empty]').hidden = count !== 0;
  }
  if (cards.length) {
    document.querySelector('[data-library-tools]').hidden = false;
    cards.forEach((card) => {
      const link = card.querySelector('h3 a');
      card.append(makeSaveButton(link.getAttribute('href'), link.textContent.trim(), null));
    });
    search.addEventListener('input', filterLibrary);
    document.querySelectorAll('[data-topic]').forEach((button) => button.addEventListener('click', () => {
      topic = button.dataset.topic;
      document.querySelectorAll('[data-topic]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      filterLibrary();
    }));
    document.querySelector('[data-library-reset]').addEventListener('click', () => {
      search.value = '';
      document.querySelector('[data-topic="all"]').click();
      search.focus();
    });
    filterLibrary();
  }

  const choices = document.querySelector('[data-finder-choices]');
  if (choices) {
    choices.hidden = false;
    const apps = {
      focus: { name: 'Temvica', path: '/temvica/', symbol: '25:00', caption: 'ONE THING AT A TIME', description: 'Focus sessions, Pomodoro tools, and ambient audio for the work in front of you.' },
      listen: { name: 'HushFlow', path: '/hushflow/', icon: 'M9 18V5l11-2v13M9 8l11-2M9 18c0 1.7-1.3 3-3 3s-3-1.3-3-3 1.3-3 3-3 3 1.3 3 3Zm11-2c0 1.7-1.3 3-3 3s-3-1.3-3-3 1.3-3 3-3 3 1.3 3 3Z', caption: 'LISTEN ON YOUR TERMS', description: 'Screen-off audio and a sleep timer for music, podcasts, and moments of quiet.' },
      protect: { name: 'Noctra', path: '/noctra/', icon: outwardArrow, caption: 'MAKE ROOM FOR LIFE', description: 'App blocking and digital boundaries to help you step away from distracting habits.' }
    };
    choices.querySelectorAll('[data-goal]').forEach((button) => button.addEventListener('click', () => {
      const app = apps[button.dataset.goal];
      choices.querySelectorAll('button').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      document.querySelector('[data-finder-app]').textContent = app.name;
      document.querySelector('[data-finder-description]').textContent = app.description;
      document.querySelector('[data-finder-symbol]').replaceChildren(app.icon ? icon(app.icon, 40) : document.createTextNode(app.symbol));
      document.querySelector('[data-finder-caption]').textContent = app.caption;
      const link = document.querySelector('[data-finder-link]');
      link.href = app.path; link.dataset.app = app.name.toLowerCase(); link.replaceChildren(document.createTextNode(`Explore ${app.name}`), icon(outwardArrow));
      const scene = document.querySelector('.finder-scene');
      if (!motion.matches) { scene.classList.remove('is-changing'); void scene.offsetWidth; scene.classList.add('is-changing'); }
    }));
  }

  const article = document.querySelector('.page-guide .article-content');
  let progress, contents = [];
  if (article) {
    const toc = document.querySelector('details.table-of-contents');
    if (toc) {
      const wide = matchMedia('(min-width: 1025px)');
      const updateContents = () => { toc.open = wide.matches; };
      wide.addEventListener('change', updateContents);
      updateContents();
    }
    progress = document.createElement('div');
    progress.className = 'reading-progress'; progress.setAttribute('aria-hidden', 'true');
    progress.append(document.createElement('span')); document.body.append(progress);
    const tools = document.createElement('div'); tools.className = 'guide-tools';
    const status = document.createElement('span'); status.className = 'guide-tool-status'; status.setAttribute('role', 'status');
    const url = location.pathname.replace(/index\.html$/, '');
    tools.append(makeSaveButton(url, document.querySelector('h1').textContent.trim(), status));
    const copy = document.createElement('button'); copy.type = 'button'; copy.textContent = 'Copy link';
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(`${location.origin}${url}`);
        status.textContent = 'Link copied.';
      } catch (_) { status.textContent = 'Copy the page address from your browser to share this guide.'; }
    });
    tools.append(copy, status);
    (document.querySelector('.article-header') || article).append(tools);
    contents = [...document.querySelectorAll('.table-of-contents a[href^="#"]')].map((link) => ({ link, target: document.getElementById(link.hash.slice(1)) })).filter((item) => item.target);
  }
  syncSaves();
  window.addEventListener('storage', (event) => {
    if (event.key === 'nextflow-theme') {
      preference = ['system', 'light', 'dark'].includes(event.newValue) ? event.newValue : 'system'; applyTheme();
    }
    if (event.key === 'nextflow-saved-guides') { saved = parseSaved(event.newValue); syncSaves(); filterLibrary(); }
  });

  const top = document.createElement('button'); top.type = 'button'; top.className = 'back-to-top'; top.hidden = true;
  top.append(icon('M12 19V5M5 12l7-7 7 7')); top.setAttribute('aria-label', 'Back to top'); document.body.append(top);
  top.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: motion.matches ? 'instant' : 'smooth' });
    const destination = document.querySelector('h1');
    if (destination) { destination.setAttribute('tabindex', '-1'); destination.focus({ preventScroll: true }); }
  });
  let scheduled = false;
  const updateReading = () => {
    scheduled = false;
    top.hidden = scrollY < 700;
    if (progress) {
      const rect = article.getBoundingClientRect();
      const start = scrollY + rect.top - 100;
      const length = Math.max(1, rect.height - innerHeight + 100);
      const fraction = Math.min(1, Math.max(0, (scrollY - start) / length));
      progress.firstElementChild.style.transform = `scaleX(${fraction})`;
      let current = contents[0];
      contents.forEach((item) => { if (item.target.getBoundingClientRect().top <= 180) current = item; });
      contents.forEach((item) => { if (item === current) item.link.setAttribute('aria-current', 'location'); else item.link.removeAttribute('aria-current'); });
    }
  };
  const queueReading = () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateReading); } };
  addEventListener('scroll', queueReading, { passive: true }); addEventListener('resize', queueReading); updateReading();

  // Animate only visible sections, once, with a safe fallback if observation is unavailable.
  if (!motion.matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.remove('reveal-pending'); entry.target.classList.add('reveal-ready'); observer.unobserve(entry.target); }
    }), { threshold: 0.08 });
    const targets = [...document.querySelectorAll('.section-head, .product-card, .feature, .author-box')].filter((element) => element.getBoundingClientRect().top > innerHeight);
    targets.forEach((element) => { element.classList.add('reveal-pending'); observer.observe(element); });
    motion.addEventListener('change', () => {
      if (motion.matches) { targets.forEach((element) => element.classList.remove('reveal-pending')); observer.disconnect(); }
    });
  }
})();
