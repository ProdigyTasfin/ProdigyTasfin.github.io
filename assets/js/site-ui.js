(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('.faq details').forEach((details) => {
    const summary = details.querySelector(':scope > summary');
    if (!summary) return;

    const answer = document.createElement('div');
    answer.className = 'faq-answer';
    const inner = document.createElement('div');
    inner.className = 'faq-answer-inner';

    [...details.children].filter((child) => child !== summary).forEach((child) => inner.append(child));
    answer.append(inner);
    details.append(answer);
    if (details.open) answer.style.height = 'auto';

    let animation;
    summary.addEventListener('click', (event) => {
      event.preventDefault();
      animation?.cancel();

      if (reducedMotion.matches) {
        details.open = !details.open;
        answer.style.height = details.open ? 'auto' : '0px';
        return;
      }

      const opening = !details.open;
      if (opening) details.open = true;
      const startHeight = opening ? 0 : answer.offsetHeight;
      const endHeight = opening ? inner.offsetHeight : 0;
      answer.style.height = `${startHeight}px`;

      animation = answer.animate(
        { height: [`${startHeight}px`, `${endHeight}px`] },
        { duration: 300, easing: 'cubic-bezier(.22, 1, .36, 1)' }
      );
      animation.onfinish = () => {
        details.open = opening;
        answer.style.height = opening ? 'auto' : '0px';
        animation = null;
      };
    });
  });
})();
