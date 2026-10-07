# Organic acquisition implementation — October 7, 2026

The implementation keeps the static GitHub Pages architecture and the existing premium palette, navigation, themes, search, saves and reading tools. It strengthens the path from a useful answer to the matching Android app. The supplied search evidence prioritizes screen-off audio/HushFlow, then sleep timers, the November/evergreen Noctra cluster, and Temvica.

## A. SEO issues discovered

The baseline had 25 self-canonical indexable pages, a complete sitemap, crawlable assets and no internal HTTP links; these were already correct. Missing pieces were known typo-route consolidation, a custom 404, consistent contextual app recommendations, commercial -> guide links, metadata/date/image alignment and a usable measurement contract. Large artwork and the mobile contents list preceded the answer. Image dimensions sometimes disagreed with their actual files, and several files exceeded 1 MB. The November article conflated an informal challenge with a product campaign. Existing FAQ schema no longer provides Google's retired FAQ rich-result feature. The audit is in [Repository audit](organic-growth-audit.md).

The screen-off CTR is about 0.74% and sleep-timer CTR about 0.18% in the supplied figures. Average positions and reporting dates were not supplied, so this is not proof that metadata caused the low CTR.

## B. Technical fixes

- Added catalog-driven, statically rendered CTA, product visual, free/Premium and related-guide fragments without adding a framework or runtime content renderer.
- Centralized Play package destinations and app/intent relationships in `content/acquisition.json`, with a `--check` synchronization mode.
- Added canonical alias mapping, a useful noindex 404 and explicit redirect exclusions from the sitemap validator.
- Added acquisition/schema/image/link checks and browser regression checks to the existing GitHub Actions Site checks workflow.
- Fixed the homepage default finder recommendation/link mismatch and kept its app attribute synchronized when switching goals.
- Made contents lists compact native disclosures on mobile, with expanded desktop navigation; kept them usable without JavaScript.
- Fixed save-button accessible names and made wide tables keyboard-focusable with named regions and a visible focus outline.
- Moved website measurement disclosure into the existing tracking section and authored its genuine October 7 revision date.

## C. Pages modified

Material content/layout changes: homepage, `/articles/`, all nine existing guides, `/hushflow/`, `/noctra/`, `/temvica/`, `/noctra/november-reset/`, and the website privacy policy. No additional indexable articles were published.

The other support/legal/app-policy/partnership pages receive the small shared measurement hook, Play-link normalization where applicable and structured-data cleanup where present. Their policy dates and sitemap lastmod were not bumped for shared-script-only changes.

New non-indexable files: `404.html` and the two known screen-off typo alias `index.html` files. New maintenance files: acquisition/redirect catalogs, responsive WebP derivatives and manifest, generation/validation scripts, four implementation/release documents plus this changelog.

## D. Redirects and canonicals

These aliases each point directly to `/articles/how-to-play-audio-with-screen-off-android/`:

- `/articles/how-id-play-audio-with-screen-off-android/`
- `/articles/how-to-play-audio-with-the-screen-off-android/`

They use immediate static meta refresh, canonical destination and noindex, with a fallback link. **They are not HTTP 301/308 responses.** GitHub Pages does not read arbitrary `.htaccess` or `_redirects` rules. Hosting-level Enforce HTTPS, slash/www behavior and response headers must be verified after deployment; the available connector cannot configure those settings. See [Release and Search Console checklist](search-console-release.md).

All 25 canonical pages retain self-reference on HTTPS, with folder trailing slashes and existing `.html` legal/support routes. No redirecting alias or 404 is in the sitemap, and no canonical article is noindex. October 7 lastmod is limited to materially revised content. Robots still allows the public pages and rendering assets and advertises the sitemap.

## E. Metadata

The winning screen-off URL, natural title and description were already appropriate and are preserved. Manufacturer troubleshooting and the screen-off-versus-powered-off distinction remain. A sourced Android media-notification clarification is added without radically rewriting the guide.

| Page | Final title / change |
| --- | --- |
| Screen-off guide | Preserved: How to Play Music With the Screen Off on Android |
| Sleep timer | Music Sleep Timer on Android: Stop Audio Automatically; description covers 30-minute stopping, locked screens and a missing built-in timer |
| HushFlow | HushFlow: Screen-Off Music & Sleep Timer for Android; offline downloads explicitly optional Premium |
| Noctra | Noctra: Android App Blocker for Focus & Screen Time |
| NNN pillar | No Nut November 2026 & No Goon November: Rules and Boundaries |
| November campaign | Noctra November Reset 2026: A 30-Day Digital Boundary |
| Blocker guide | Removed the fixed method count after consolidating Noctra recommendations; seven practical steps remain |
| Library | Intent-based description, with synchronized social/schema copy and visible card order |

All indexable page titles and descriptions are unique. Article H1/JSON-LD headline and material revision dates are synchronized. Social image references use lighter derivatives with corrected known dimensions. Medical article attribution and sourced guidance remain.

## F. Structured data

Kept accurate Article/BlogPosting, BreadcrumbList, MobileApplication, CollectionPage, Organization and WebSite data. Library ItemList positions, URLs and names now match the visible cards and are covered by the sync check. Article dates, author/team URLs, headlines and image dimensions align with visible content. Removed oversized schema keyword lists, FAQPage blocks and unnecessary app-offer availability claims. The free-download offers remain because the pages visibly describe free download.

No rating, review, install count or fabricated price was added. Valid MobileApplication data alone does not establish eligibility for a Google software-app rich result without its other requirements. Visible FAQs remain useful even after removing schema; see [Google's documentation updates](https://developers.google.com/search/updates) and [software-app requirements](https://developers.google.com/search/docs/appearance/structured-data/software-app).

## G. Internal links and intent ownership

| Query/intent family | Primary informational URL | Commercial relationship |
| --- | --- | --- |
| Screen-off audio / locked-phone music | `/articles/how-to-play-audio-with-screen-off-android/` | HushFlow |
| Music sleep timer / automatic audio stop | `/articles/how-to-use-a-music-sleep-timer-on-android/` | HushFlow |
| How to block distracting apps | `/articles/how-to-block-distracting-apps-on-android/` | Noctra; commercial app-blocker intent belongs on `/noctra/` |
| Stop doomscrolling | `/articles/how-to-reduce-doomscrolling-on-android/` | Noctra |
| Student digital detox | `/articles/digital-detox-plan-for-students/` | Noctra |
| NNN / No Goon November 2026 rules | `/articles/no-goon-november-no-nut-november-2026/` | November Reset -> Noctra |
| Noctra campaign eligibility/enrollment | `/noctra/november-reset/` | Noctra Play |
| Responsible adult-content habit support | `/articles/how-to-remove-porn-addiction/` | Noctra as a limited boundary tool, never treatment |
| Study Pomodoro technique | `/articles/how-to-use-pomodoro-for-studying/` | Temvica |
| Coding Pomodoro workflow | `/articles/pomodoro-timer-for-coding/` | Temvica |

Each guide has one primary app relationship. Product pages now link back to all relevant guides; existing lateral related-reading links remain. The library features screen-off/sleep guides first, preserves topical filters/search/saves, adds a November Reset filter, and includes the relevant app route on every card. No sitewide keyword-link directory was added.

## H. Conversion improvements

Each of the nine guides has a contextual recommendation **after a useful answer/solution** and a shorter end action, with one main button, three relevant mid-article benefits, a subordinate product-details link, studio ownership disclosure and limitations. HushFlow recommendations distinguish supported background playback, built-in timer and Premium offline downloads. The timer does not control an unrelated app. Noctra copy does not diagnose, treat or guarantee habit changes. The November pillar distinguishes the informal challenges, Noctra's campaign and the Android app, including in its FAQs.

The three commercial heroes explain the Android use case, free download/ads/IAP and a clear Google Play action. Free/Premium comparisons, authentic official Play product visuals, privacy/support links and related guides reduce decision friction. Existing maintained campaign pricing/market limitations remain; no new price or urgency was invented. Campaign sticky actions appear after its hero and hide when the footer is visible.

## I. Measurement

Added a bounded local event interface for page views, CTA exposures, article -> app/product transitions, product -> Play, pricing interest and November actions. Events identify app, canonical source path, placement and article slug without query strings or visitor identifiers. Consent-gated optional forwarding respects Do Not Track/GPC, catches collector errors and avoids replay/double counting. CTA impression context distinguishes primary versus secondary actions.

**No analytics collector or aggregate dashboard is configured.** Installs and purchases are unavailable without verified app/Play reporting. No unsupported referrer attribution was added. [Measurement setup and formulas](acquisition-measurement.md) explain what to connect and how to avoid labeling all website clicks as organic installs.

## J. Performance, mobile and accessibility

26 originals are preserved. Their largest served derivative versions total **1,832,164 bytes**, versus **21,973,674 bytes** for those originals: **91.7% smaller combined**. This is an asset comparison, not a measured speed/Core Web Vitals claim. Responsive widths, true aspect ratios, srcset/sizes, lazy below-fold artwork and corrected social/schema dimensions reduce unnecessary transfer and layout-shift risk. Original artwork remains available; no logo or illustration was regenerated.

Product headings/heroes are smaller on phones. Informational answers precede artwork; mobile contents no longer form a full-screen wall before the title. Primary app buttons have suitable mobile size, and the existing themes, reduced motion, menu, native FAQs and no-JS paths remain functional. Wide tables can receive keyboard focus, and save controls' accessible names contain their visible text.

Validation commands and CI cover local URLs/anchors, canonical/sitemap/schema alignment, catalog/image integrity, JavaScript syntax, three-width light/dark layouts, filters/saves/reading tools, nine contextual funnels, real Play/pricing navigation, alias/404 recovery and measurement privacy boundaries. A separate local axe-core review checks all 26 rendered pages in both themes; this automated review does not replace manual assistive-technology testing or deployed field performance measurement.

## K. Deliberately retained or deferred

Retained the framework, official NextFlow logo URL, `support@nextflow-apps.com`, winning article URL/content, legal `.html` routes, author identities, maintained pricing, themes and browsing tools. No mass articles, fake ratings, medical promises, new unverified prices or artificial date refreshes were added.

Palma is a real BOOX Android device, but its query does not establish HushFlow compatibility; no untested device claim or doorway page is published. No Android repository/Install Referrer integration, collector account, Search Console account or editable host settings were supplied. Those configuration steps are documented accurately rather than presented as completed.

## L. Ten-item future content plan

[Content roadmap](content-roadmap.md) provides ten scored candidates, full query/intent/URL/app/conversion/internal-link details, distinct-page justification and cannibalization gates. Existing winners come first; overlapping candidates stay as existing-page improvements unless original depth and separate intent justify publication.

## M. Manual Search Console actions

[Release checklist](search-console-release.md): confirm Pages deployment/HTTPS and response codes; revalidate sitemap; inspect priority canonical URLs and request indexing for actual revisions; inspect HTTP/typo/non-slash variants; monitor selected canonicals and duplicate exclusions. Review early technical signals after seven days, then comparable query/device/country/position cohorts at 14 and 28 days, with November seasonality separate.

## N. Compare outcomes

For every priority page, compare impressions, clicks, CTR, average position and query mix; then measured article -> product transitions, Play clicks, primary CTA CTR and pricing interest. Installs and paid conversions are **unavailable**, rather than zero, until reliable app/Play attribution is connected. Preserve the supplied baseline and establish an event baseline only after activating a real collector. The [release report](search-console-release.md) includes the supplied page figures and derived CTR; [measurement definitions](acquisition-measurement.md) explain denominators and consent limits.
