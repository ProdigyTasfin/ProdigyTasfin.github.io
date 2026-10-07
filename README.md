# NextFlow Apps website

Static HTML, CSS and JavaScript hosted at https://nextflow-apps.com/ using GitHub Pages. There is no application build step.

## Preview and validate

```sh
python -m http.server 8000
```

Open http://localhost:8000/. To check local links, fragments, sitemap coverage, SEO metadata and JavaScript syntax (requires Python 3.12+ and Node.js):

```sh
python .github/scripts/check_site.py
python .github/scripts/sync_acquisition.py --check
python .github/scripts/optimize_images.py --check
python .github/scripts/check_acquisition.py
```

To run responsive browser checks:

```sh
python -m pip install playwright==1.62.0
python -m playwright install chromium
python .github/scripts/check_ui.py
python .github/scripts/check_premium.py
python .github/scripts/check_acquisition_ui.py
```

`CHROMIUM_PATH` can select an already installed Chromium binary. Browser tests block external services and test local site files. The Site checks workflow runs these validators on pull requests and pushes to main; it does not replace the managed Pages deployment workflow.

## Organic acquisition maintenance

The site remains static and crawlable without JavaScript. `content/acquisition.json` owns app package/Play URLs, one primary app per guide and contextual CTA copy. Marked HTML fragments are generated with:

```sh
python .github/scripts/sync_acquisition.py
```

Edit article content normally, then synchronize to keep product guide links, library schema and catalog fragments current. Use `--check` in CI; do not edit generated fragments alone. For a new guide, add its catalog relationship, CTA markers, library card, sitemap entry and real authored metadata/date. Preserve existing canonical URLs and use descriptive app-specific actions.

Original artwork is retained. To add/change local WebP artwork, install Pillow in a local development environment and regenerate responsive variants:

```sh
python -m pip install Pillow
python .github/scripts/optimize_images.py
python .github/scripts/sync_acquisition.py
```

Commit original artwork, responsive derivatives and their manifest together. Image validation in CI uses only the standard library and verifies source/derivative hashes. Never change all content dates simply because assets or shared scripts were regenerated.

Measurement hooks are local by default; no analytics collector, install or purchase attribution is configured. See [measurement setup](docs/acquisition-measurement.md), [audit](docs/organic-growth-audit.md), [A–N changelog](docs/organic-growth-changelog.md), [ten-candidate content roadmap](docs/content-roadmap.md) and [hosting/Search Console release steps](docs/search-console-release.md).

`content/redirects.json` documents the two known static redirect fallbacks. They are immediate meta refreshes, not HTTP 301/308 responses. Keep aliases and `404.html` out of the sitemap. Hosting-level HTTPS/www/slash response verification is a separate release step.

## Appearance and browsing

The shared palette and layout refinements are in `assets/css/premium.css`. Every public page has a small startup script to apply the saved appearance before rendering; `assets/js/premium.js` handles System, Light and Dark choices and updates when the device appearance changes. Motion respects `prefers-reduced-motion`.

The homepage app finder links visitors to the product that fits their goal. The article library supports search, topic filters and saved guides. Articles include save and copy-link controls, reading progress and highlighted contents links. Appearance (`nextflow-theme`) and saved guide URLs (`nextflow-saved-guides`) use browser local storage on the current device, without an account or server. If storage is unavailable, the controls work for the current visit and explain the limitation. Articles and navigation remain usable without JavaScript.

## Deployment

GitHub Pages currently publishes the `main` branch from the repository root. Keep `CNAME` and `.nojekyll` at the root. `.well-known/assetlinks.json` must remain available for Android app associations. Review and merge a pull request to publish its changes; a branch alone is not deployed.

In the Actions tab, open the latest **pages build and deployment** run. A successful build/upload followed by a queued deploy, `The job was not acquired by Runner of type hosted`, or an internal server error can indicate GitHub infrastructure problems. Check https://www.githubstatus.com/ before changing site configuration. The October 6, 2026 deployment delay (Asia/Dhaka) had these runner-assignment errors; the latest run subsequently completed successfully.

Wait for an active run rather than cancelling it repeatedly. After a failed run and service recovery, use **Re-run all jobs** on the latest main-branch Pages run. Rebuilding refreshes the short-lived Pages artifact. Confirm the deployment completed before checking the public URL. If build/upload fails instead, inspect that step's logs and fix its specific error.

The shared navigation controller is `assets/js/main.js`; FAQ animation is `assets/js/site-ui.js`; shared interaction and footer styles are in `assets/css/site-ui.css`. Keep policy revision dates authored in the HTML rather than replacing them with the visitor's date.
