# Repository audit — October 7, 2026

Audited before implementation at main commit `bc734c0`. The supplied Search Console data is a user-provided baseline; its reporting dates, average positions, device/country splits and installed-app attribution were not supplied. Its CTR values describe performance, not proof of a specific cause.

## Architecture and existing foundations

- GitHub Pages serves plain HTML/CSS/JavaScript from the repository root, with `.nojekyll`, `CNAME` and no application build/framework/router. Folder `index.html` files provide trailing-slash product/article routes; legal/support pages intentionally use `.html` URLs.
- 25 public HTML pages, nine guides, three product landing pages and a dedicated Noctra November 2026 campaign. The Google verification file, `app-ads.txt` and Android `.well-known/assetlinks.json` are operational assets.
- No server templates or reusable content components. Page styles and metadata are mostly inline; navigation, FAQ behavior and light/dark appearance have shared controllers/styles. Search, topic filters, device-local guide saves and reading tools already work.
- All public pages have one H1, self-referencing HTTPS canonical URLs and descriptions. The manually maintained sitemap already covers all 25 pages without HTTP URLs. Robots allows rendering assets and advertises the sitemap. No accidental public noindex or HTTP internal references were found.
- Static validator passes at baseline. Structured data includes Article, BreadcrumbList, MobileApplication, Organization, WebSite, ItemList and FAQPage. No fabricated rating/review data was found.
- Product package IDs are HushFlow `com.tasfin.hushflow`, Noctra `com.tasfin.noctra`, and Temvica `com.tasfin.focusflow`. Google Play listings were fetched and confirm the core screen-off/timer, blocking and study features. Their external listings still show the previous Gmail support contact in the fetched copy; verify/update that separately in Play Console.
- Product pages already have prominent Google Play buttons, privacy links, FAQs, free/Premium references and feature explanations. The screen-off guide already has a strong title, direct answer, manufacturer troubleshooting and powered-off-device distinction. The sleep-timer guide also already answers the key variants. These are assets to retain.

## Issues found

1. Screen-off CTR is approximately **0.74%** (158 / 21,310); sleep-timer CTR approximately **0.18%** (5 / 2,727). Ranking/query/device context is needed before assigning causality. Improve usefulness and conversion placement; protect the winning URL and content.
2. Known typo/alternate screen-off routes have no source files or redirect mapping. Unknown routes have no custom 404. GitHub Pages cannot apply arbitrary repository `_redirects` or `.htaccess` rules.
3. HTTPS enforcement/host-level response codes cannot be verified or configured through the available repository connector. A fetched HTTP sleep-timer URL did not expose a verifiable status/redirect chain. Settings verification remains a hosting step.
4. Article recommendations are inconsistently placed. Many final blocks send visitors toward the whole app portfolio, while direct Play actions are secondary to generic app-page actions. Product pages lack a consistent related-guides section.
5. Hero artwork appears before the direct answer. Large product heroes delay the main action on mobile.
6. Several WebP assets are 0.9–2.1 MB each despite being displayed in narrow article columns/cards. The asset tree is approximately 27 MB. Many declared image dimensions differ from actual pixel dimensions; one portrait is declared as a landscape hero.
7. Article headline, visible updated date, JSON-LD and image metadata drift in places. The November article labels an informal term as if owned exclusively by Noctra; the named app campaign needs to be distinguished clearly. Several generic author boxes refer to an organization as “He.”
8. FAQPage markup adds maintenance despite Google's May/June 2026 FAQ rich-result removal. MobileApplication free-download offers exist, but no verified ratings qualify the pages for a software-app rich-result promise.
9. No live analytics collector, account ID, consent manager or Android Install Referrer implementation is configured in this repository. An unused November script queues local events and copies arbitrary incoming UTM parameters, but the campaign does not load it. There is no reliable aggregated outbound funnel measurement.
10. Google Play URLs and CTA copy are scattered across HTML, and no drift check relates each guide to its intended app. There is no documented query-to-primary-URL mapping or prioritized content roadmap.

## Research and scope decisions

BOOX's official Palma product page confirms a real Android ePaper product; the query is plausibly device troubleshooting intent. It does not establish HushFlow compatibility or successful testing on that model. No competitor doorway page or untested Palma claim will be added.

The repository supports static, crawlable component generation. Keep the existing design, logo and support email, provide a small catalog-driven synchronization script, serve responsive image derivatives, and implement documented zero-second static redirect fallbacks for the two known alternate routes. Keep permanent HTTP redirects/HTTPS enforcement as explicit hosting verification requirements rather than inventing unsupported rules.

Measurement will be a local event interface with an optional consent-gated adapter, without a new third-party script, fingerprint, session identifier or fabricated install/purchase attribution. A real collector still needs configuration before aggregate reporting exists.

## Sources checked

- [GitHub Pages HTTPS enforcement](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [Google redirect guidance](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Google Search documentation changelog: FAQ feature removal](https://developers.google.com/search/updates)
- [Software application structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
- [Android notification permission: media-session exemption](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
- [BOOX Palma product page](https://shop.boox.com/products/palma)
- The three Google Play URLs in `content/acquisition.json`.
