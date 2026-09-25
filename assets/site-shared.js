// Animate FAQ disclosure height without stretching neighboring grid cards.
document.querySelectorAll('.faq details').forEach(details => {
  const summary = details.querySelector('summary');
  if (!summary) return;

  summary.addEventListener('click', event => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !details.animate) return;
    event.preventDefault();

    const startHeight = `${details.offsetHeight}px`;
    const opening = !details.open;
    if (opening) details.open = true;

    const styles = getComputedStyle(details);
    const closedHeight = summary.offsetHeight
      + parseFloat(styles.paddingTop)
      + parseFloat(styles.paddingBottom)
      + parseFloat(styles.borderTopWidth)
      + parseFloat(styles.borderBottomWidth);
    const endHeight = opening ? `${details.scrollHeight}px` : `${closedHeight}px`;

    details.getAnimations().forEach(animation => animation.cancel());
    const animation = details.animate(
      [{ height: startHeight }, { height: endHeight }],
      { duration: 260, easing: 'cubic-bezier(.2, .8, .2, 1)' }
    );
    animation.onfinish = () => {
      details.open = opening;
      details.style.height = '';
    };
  });
});
