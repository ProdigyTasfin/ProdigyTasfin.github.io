# Salvera website integration — October 18, 2026

## Result and authorization

Salvera is integrated locally as the fourth NextFlow Apps product. The current NextFlow palette, Inter typography, CSS tokens, corporate logo, existing product icons, theme behavior and navigation patterns remain. No new framework or Salvera-specific color theme was introduced.

The initial local checkout was the merged organic-acquisition work. A read-only fetch found the required official PNG in main commit `1083196`; the clean local checkout was fast-forwarded to that existing commit before implementation. The implementation was initially kept local under the original instruction. The user subsequently authorized making it publicly visible; it is now being published through a checked pull request and the existing GitHub Pages deployment workflow.

The user explicitly waived the requirement to inspect the unavailable Windows Android/backend projects. Their contents were not inferred, copied or represented as audited. The website uses the brief as the development scope, with in-development status and truthful limits on unknown behavior.

## 1. Existing HTML audited

All 29 existing HTML documents were inspected for page structure, canonical/robots metadata, shared scripts/styles, navigation, footers, product references and local links. That includes 26 rendered content pages, two static redirect aliases and the Google verification document. Existing static and acquisition validators passed before changes.

Audited documents:

- `404.html`
- `articles/digital-detox-plan-for-students/index.html`
- `articles/how-id-play-audio-with-screen-off-android/index.html`
- `articles/how-to-block-distracting-apps-on-android/index.html`
- `articles/how-to-play-audio-with-screen-off-android/index.html`
- `articles/how-to-play-audio-with-the-screen-off-android/index.html`
- `articles/how-to-reduce-doomscrolling-on-android/index.html`
- `articles/how-to-remove-porn-addiction/index.html`
- `articles/how-to-use-a-music-sleep-timer-on-android/index.html`
- `articles/how-to-use-pomodoro-for-studying/index.html`
- `articles/index.html`
- `articles/no-goon-november-no-nut-november-2026/index.html`
- `articles/pomodoro-timer-for-coding/index.html`
- `google73691dbd946c0065.html`
- `hushflow/index.html`
- `hushflow/privacy-policy.html`
- `index.html`
- `noctra/data-deletion.html`
- `noctra/index.html`
- `noctra/november-reset/index.html`
- `noctra/privacy-policy.html`
- `partnerships.html`
- `privacy-policy.html`
- `refund-policy.html`
- `support.html`
- `temvica/data-deletion.html`
- `temvica/index.html`
- `temvica/privacy-policy.html`
- `terms-policy.html`

Shared assets and maintenance files audited include `assets/css/style.css`, `site-ui.css`, `premium.css`, `assets/js/main.js`, `site-ui.js`, `premium.js`, `acquisition.js`, `november-reset.js`, the acquisition/redirect catalogs, sitemap, robots, CNAME, Pages markers and validation workflow. No AGENTS.md instructions were found in the accessible workspace.

## 2. Existing files modified

- `.github/scripts/check_premium.py`
- `.github/scripts/check_ui.py`
- `.github/workflows/site-checks.yml`
- `404.html`
- `README.md`
- `articles/digital-detox-plan-for-students/index.html`
- `articles/how-to-block-distracting-apps-on-android/index.html`
- `articles/how-to-play-audio-with-screen-off-android/index.html`
- `articles/how-to-reduce-doomscrolling-on-android/index.html`
- `articles/how-to-remove-porn-addiction/index.html`
- `articles/how-to-use-a-music-sleep-timer-on-android/index.html`
- `articles/how-to-use-pomodoro-for-studying/index.html`
- `articles/index.html`
- `articles/no-goon-november-no-nut-november-2026/index.html`
- `articles/pomodoro-timer-for-coding/index.html`
- `assets/js/premium.js`
- `hushflow/index.html`
- `hushflow/privacy-policy.html`
- `index.html`
- `noctra/data-deletion.html`
- `noctra/index.html`
- `noctra/november-reset/index.html`
- `noctra/privacy-policy.html`
- `partnerships.html`
- `privacy-policy.html`
- `refund-policy.html`
- `sitemap.xml`
- `support.html`
- `temvica/data-deletion.html`
- `temvica/index.html`
- `temvica/privacy-policy.html`
- `terms-policy.html`

All 26 existing rendered HTML pages receive a Salvera primary-navigation entry and a four-product footer. Article content and existing app/app-policy `<main>` content were compared with the baseline and remain exactly unchanged. The two aliases and verification document are unchanged.

Homepage changes add the fourth card, a working Family care finder choice, company product references, release-status distinctions and synchronized four-product ItemList/Organization metadata. The product grid remains the same card design in a balanced two-column arrangement on desktop and one column on smaller screens.

The existing refund policy receives navigation updates and one missing `</div>` repair discovered by structural HTML validation. Its billing text and August 2026 revision date remain unchanged. No Salvera billing product was invented.

## 3. New Salvera pages and URL structure

| Local file | Public URL after a separately approved deployment | Purpose |
| --- | --- | --- |
| `salvera/index.html` | `https://nextflow-apps.com/salvera/` | In-development product overview, intended features, three modes, workflow, privacy/safety and FAQs |
| `salvera/privacy-policy.html` | `https://nextflow-apps.com/salvera/privacy-policy.html` | Pre-release privacy information and contact; distinguishes unknown app flows from other products’ policies |
| `salvera/data-deletion.html` | `https://nextflow-apps.com/salvera/data-deletion.html` | Real email request path, account/local/cloud distinction and unverified deletion/retention details |
| `salvera/terms.html` | `https://nextflow-apps.com/salvera/terms.html` | Medication tracking limits, reminder reliability, stock estimates, consent and account responsibilities |
| `salvera/support.html` | `https://nextflow-apps.com/salvera/support.html` | Contact, sign-in, reminders, Health Connect, invitations, stock/refill and privacy/deletion assistance |

These are the routes included in the approved publication. Deployment and live checks are recorded separately from the implementation tests. The five intended indexable routes have self-canonicals and sitemap entries. No alternate Salvera slugs or duplicate pages were added.

## 4. Official logo and assets

The mandatory repository image `Minimal Red Heartcare Triangle Icon.png` is preserved unchanged. Its byte-for-byte copy is `assets/salvera/logo.png` (1254 × 1254). Derived PNGs use the same artwork, colors and full aspect ratio, without cropping, redrawing or recoloring:

| Asset | Use | Bytes |
| --- | --- | ---: |
| `assets/salvera/logo-32.png` | Salvera favicon | 1,388 |
| `assets/salvera/logo-96.png` | Homepage card, app finder and privacy directory | 7,724 |
| `assets/salvera/logo-180.png` | Salvera Apple touch icon | 23,330 |
| `assets/salvera/logo-192.png` | Product hero | 26,324 |
| `assets/salvera/logo-384.png` | Higher-resolution hero, Open Graph/Twitter and structured data | 115,824 |

`assets/salvera/manifest.json` records the source hash, exact original copy and derivative hashes/dimensions. The product validator checks PNG signatures, sizes, hashes and aspect ratios. Reserved dimensions and `object-fit: contain` protect layout and prevent clipping the artwork. No simulated screenshots or alternative logos are used. Company-wide favicons and the other three app icons remain unchanged.

## 5. Navigation and layout

- All 31 rendered pages now expose Salvera in their shared primary navigation and four-product footers. Header behavior remains responsive and keyboard-accessible.
- All Salvera pages provide a five-link information menu near the top. Their footers also link directly to Salvera support, privacy, terms and account deletion, while retaining company legal references.
- Homepage finder includes a real Family care action and the official Salvera image; it updates the recommendation, link and app attribute correctly.
- `content/products.json` owns the four-product inventory. `sync_products.py` keeps crawlable navigation and homepage ItemList schema synchronized. The three-app acquisition catalog continues to represent only apps with verified Play destinations.
- `assets/css/product-pages.css` contains layout rules using existing tokens and patterns. It does not define a new color palette, introduce a new font or replace theme behavior.

## 6. Policy, support and partnership changes

The global support page links to Salvera support, privacy and deletion. The global privacy page clearly separates the existing apps’ data statements from Salvera’s pre-release information. General Terms link to Salvera-specific terms and include the fourth product. Materially revised global privacy and terms dates are authored as October 18, 2026; existing app-specific policy dates remain unchanged.

Salvera privacy and deletion pages do **not** pretend an Android/backend audit was performed. They identify app-specific storage, synchronization, security, retention, backup and deletion behavior that still needs confirmation. They make no unsupported encryption, end-to-end encryption, regulatory certification, rating, install-count or pricing claim. A website statement is not proof of app-side behavior or Google Play compliance.

The deletion action opens an email addressed to `support@nextflow-apps.com` with a clear Salvera account/data deletion subject. The address and manual fallback are visible. Sending the email is explicitly not represented as completed deletion. There is no pretend form, unverified endpoint or invented in-app sequence. A real app-side deletion process, caregiver-access revocation and actual retention/backups remain external implementation facts to confirm.

Partnerships now identifies Salvera and a proposed pharmacy-integration opportunity. Refill ordering, prescription delivery and delivery tracking are explicitly not represented as operational services. No DiRx Health or other pharmacy agreement is claimed.

## 7. SEO and indexability

- The five Salvera pages use unique descriptive titles/descriptions, one H1, canonical URLs, viewport metadata, original-logo social previews and accurate BreadcrumbList/WebPage data.
- The overview includes SoftwareApplication information limited to name, Android, health category, project description and image. It has no unverified offer, download URL, rating, review or software version.
- Homepage ItemList contains four products in the same order as the visible cards. Organization copy distinguishes Salvera’s development status.
- Sitemap coverage grows from 25 to 30 canonical indexable pages. Lastmod changes are limited to five new pages and materially changed home, support, partnerships, global privacy and terms content. Shared navigation-only changes do not manufacture article freshness.
- Robots, CNAME, `.nojekyll`, verification HTML, Android association files and existing redirect aliases remain intact. No unsupported GitHub Pages server-redirect rules were added. Existing HTTP/www/slash enforcement remains a host-level setting, rather than something claimed fixed by these local files.
- Existing article intent relationships, metadata, published/updated dates, conversion components and Google Play destinations remain unchanged.

## 8. Tests actually run

| Check | Result |
| --- | --- |
| Structural HTML with html-validate 10.17.0 | 34 documents pass eight structural/attribute/content rules; includes aliases and verification |
| `check_site.py` | 30 canonical pages; local links, anchors, metadata, JSON-LD, JS syntax, sitemap and Pages markers pass |
| `sync_products.py --check` | Navigation and four-product schema synchronized |
| `check_products.py` | 31 shared headers/footers, five routes, real mailto request and exact PNG provenance pass |
| `check_acquisition.py` | Unique metadata, nine guide relationships, 46 canonical Play links, truthful schema and responsive images pass |
| `sync_acquisition.py --check` | Existing conversion fragments and Play links remain synchronized |
| `optimize_images.py --check` | Existing 26-image responsive manifest and hashes pass |
| `check_ui.py` | 31 rendered pages at 320/768/1440px; menus, native FAQ, reduced motion, campaign action, policy dates and no-JS behavior pass |
| `check_premium.py` | Light/dark layouts, persistence, system theme, filters/saves, all four finder choices, reading tools, blocked storage and no-JS fallbacks pass |
| `check_acquisition_ui.py` | Nine article funnels, existing app Play/pricing actions, aliases/404 and consent/DNT/GPC boundaries pass |
| `check_salvera_ui.py` | Five routes at 320/390/768/1024/1440px in both themes; product discovery, near-top navigation, policy footer, real local logo loading, mailto request and no-JS behavior pass |
| axe-core 4.14.0 local review | Zero automated WCAG 2/2.1 A/AA violations across 31 pages in both themes; final six changed pages rechecked in both themes with zero violations |
| Preservation comparison | Existing article/app/app-policy main content exactly matches baseline; refund policy text unchanged |
| `git diff --check` | Pass |

Browser checks use local Chromium and block external services for reproducibility. All new local PNG assets were verified to load; existing remote company/product assets were preserved, not independently certified by these offline checks. Mobile screenshots were visually inspected. Automated accessibility rules do not establish complete accessibility, and local asset checks do not establish deployed Core Web Vitals.

The CI workflow is updated with portfolio, structural HTML and Salvera browser checks. The checks above were executed locally before publication. GitHub CI and Pages deployment must also complete before reporting the new routes as live. README contains the normal validation commands and development-only HTML validation setup; no HTML-validation library is shipped to visitors.

## 9. Unverified or intentionally omitted functionality

- No accessible Salvera Google Play listing was verified, so no store/package URL, public download, price, subscription, review or rating was added.
- Development scope comes from the supplied brief, not a claim of independently tested Android features. Medication/dose/inventory/refill/Care Circle/check-in/Health Connect/offline capabilities are labeled as development scope. Appointment and multi-device behavior are not promoted as verified features.
- Room/DataStore contents, Cloudflare Workers/D1 data flows, Resend email, encryption at rest/in transit, diagnostics, provider retention, authenticated account deletion and caregiver revocation were not verified because the user waived source inspection. No provider-specific assurances were fabricated.
- The email request route works as a website action. Actual deletion fulfillment, authenticated confirmation and retention/backups require the developer’s real process; no completed deletion or specific erasure deadline is promised.
- Product policy text remains explicitly pre-release information, not a claim of audited production data handling or Play compliance.
- No pharmacy partnership or live ordering/delivery/tracking integration is asserted.
- No secrets, real patient records or private invitation tokens were added. There are no health-record input fields, new analytics collectors or backend account actions on these pages.

## 10. New files

- `.github/scripts/check_html.cjs`
- `.github/scripts/check_products.py`
- `.github/scripts/check_salvera_ui.py`
- `.github/scripts/sync_products.py`
- `assets/css/product-pages.css`
- `assets/salvera/logo-180.png`
- `assets/salvera/logo-192.png`
- `assets/salvera/logo-32.png`
- `assets/salvera/logo-384.png`
- `assets/salvera/logo-96.png`
- `assets/salvera/logo.png`
- `assets/salvera/manifest.json`
- `content/products.json`
- `salvera/data-deletion.html`
- `salvera/index.html`
- `salvera/privacy-policy.html`
- `salvera/support.html`
- `salvera/terms.html`
- `docs/salvera-integration.md` (this report)

## Maintenance and review

Run the sync/check commands in README when adding products. Use the official asset manifest rather than replacing logos. Keep app-data statements separate from website preferences and local measurement hooks. Replace pre-release policy specifics only with facts confirmed for the actual app/backend build, and verify a public Play listing before adding a download action.

The user subsequently approved publication by asking to make the changes publicly visible. Publish through a pull request, verify CI, merge to main and confirm the resulting Pages deployment; do not treat an open pull request alone as a live website update.

## Visual refinement — October 20, 2026

The five Salvera pages now use a shared product identity bar and readable, formatted HTML. The overview adds a balanced official-logo panel, numbered feature cards, three care roles, a five-step workflow and the existing animated FAQ pattern. Support has direct topic links; support and deletion pages offer progressive copy-email controls. Policies have a responsive native contents disclosure, desktop sidebar and section highlighting. Core navigation and email links work without JavaScript.

The shared logo frame now controls its image size, aspect ratio and rounded clipping on every rendered page, including mobile. All official image sources and Salvera asset hashes are preserved. Salvera remains labeled in development; this visual update does not announce a release or confirm app behavior. Existing policy dates remain unchanged.

Validation covers all 31 rendered pages in both themes at mobile, tablet and desktop widths, logo frame/image geometry, the five Salvera routes at five widths, contents navigation, clipboard success, no-JavaScript access, existing product funnels, structural HTML, internal links, metadata, sitemap and asset provenance. Automated WCAG A/AA checks on the Salvera pages found no violations after correcting contact-panel contrast.
