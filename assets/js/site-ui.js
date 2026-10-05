/* Optional FAQ animation; native details still work without this script. */
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
    let animation;
    let desiredOpen = details.open;
    const settle = () => {
      animation?.cancel();
      animation = null;
      details.open = desiredOpen;
      answer.style.height = desiredOpen ? 'auto' : '0px';
    };
    settle();
    summary.addEventListener('click', (event) => {
      event.preventDefault();
      const startHeight = answer.getBoundingClientRect().height;
      desiredOpen = !desiredOpen;
      animation?.cancel();
      if (reducedMotion.matches || !answer.animate) {
        settle();
        return;
      }
      // Keep contents laid out while closing and reverse from their current height.
      details.open = true;
      answer.style.height = `${startHeight}px`;
      animation = answer.animate(
        { height: [`${startHeight}px`, `${desiredOpen ? inner.getBoundingClientRect().height : 0}px`] },
        { duration: 250, easing: 'cubic-bezier(.22, 1, .36, 1)' }
      );
      animation.onfinish = settle;
    });
    details.addEventListener('toggle', () => {
      if (!animation) {
        desiredOpen = details.open;
        answer.style.height = desiredOpen ? 'auto' : '0px';
      }
    });
    reducedMotion.addEventListener('change', settle);
  });
})();
