/* Progressive enhancements: every page link and email route works without JS. */
(() => {
  const contents = document.querySelector("[data-policy-contents]");
  if (contents) {
    const desktop = matchMedia("(min-width: 1101px)");
    const setContents = () => {
      contents.open = desktop.matches;
    };
    setContents();
    desktop.addEventListener("change", setContents);
    const links = [...contents.querySelectorAll('a[href^="#"]')];
    const sections = links.map((link) =>
      document.getElementById(link.hash.slice(1)),
    );
    let pending = false;
    const update = () => {
      pending = false;
      let active = 0;
      // Native anchors account for both document padding and section margins.
      const documentOffset =
        parseFloat(
          getComputedStyle(document.documentElement).scrollPaddingTop,
        ) || 0;
      const sectionOffset = sections[0]
        ? parseFloat(getComputedStyle(sections[0]).scrollMarginTop) || 0
        : 0;
      const readingLine = documentOffset + sectionOffset + 8;
      sections.forEach((section, i) => {
        if (section && section.getBoundingClientRect().top <= readingLine)
          active = i;
      });
      links.forEach((link, i) => {
        if (i === active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    };
    addEventListener(
      "scroll",
      () => {
        if (!pending) {
          pending = true;
          requestAnimationFrame(update);
        }
      },
      { passive: true },
    );
    update();
  }
  const copy = document.querySelector("[data-email-copy]");
  if (copy && navigator.clipboard && window.isSecureContext) {
    copy.hidden = false;
    const button = copy.querySelector("[data-copy-email]");
    const status = copy.querySelector("[data-copy-status]");
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText("support@nextflow-apps.com");
        status.textContent = "Email address copied.";
      } catch (_) {
        status.textContent = "Please copy support@nextflow-apps.com manually.";
      }
    });
  }
})();
