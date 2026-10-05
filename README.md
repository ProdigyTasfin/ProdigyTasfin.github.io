# NextFlow Apps website

Static HTML, CSS and JavaScript hosted at https://nextflow-apps.com/ using GitHub Pages. There is no application build step.

## Preview and validate

```sh
python -m http.server 8000
```

Open http://localhost:8000/. To check local links, fragments, sitemap coverage, SEO metadata and JavaScript syntax (requires Python 3.12+ and Node.js):

```sh
python .github/scripts/check_site.py
```

To run responsive browser checks:

```sh
python -m pip install playwright==1.62.0
python -m playwright install chromium
python .github/scripts/check_ui.py
```

`CHROMIUM_PATH` can select an already installed Chromium binary. Browser tests block external services and test local site files. The Site checks workflow runs both validators on pull requests and pushes to main; it does not replace the managed Pages deployment workflow.

## Deployment

GitHub Pages currently publishes the `main` branch from the repository root. Keep `CNAME` and `.nojekyll` at the root. `.well-known/assetlinks.json` must remain available for Android app associations. Review and merge a pull request to publish its changes; a branch alone is not deployed.

In the Actions tab, open the latest **pages build and deployment** run. A successful build/upload followed by a queued deploy, `The job was not acquired by Runner of type hosted`, or an internal server error can indicate GitHub infrastructure problems. Check https://www.githubstatus.com/ before changing site configuration. The October 6, 2026 deployment delay (Asia/Dhaka) had these runner-assignment errors; the latest run subsequently completed successfully.

Wait for an active run rather than cancelling it repeatedly. After a failed run and service recovery, use **Re-run all jobs** on the latest main-branch Pages run. Rebuilding refreshes the short-lived Pages artifact. Confirm the deployment completed before checking the public URL. If build/upload fails instead, inspect that step's logs and fix its specific error.

The shared navigation controller is `assets/js/main.js`; FAQ animation is `assets/js/site-ui.js`; shared interaction and footer styles are in `assets/css/site-ui.css`. Keep policy revision dates authored in the HTML rather than replacing them with the visitor's date.
