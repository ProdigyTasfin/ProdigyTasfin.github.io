# Deployment, indexing and comparison checklist

## Hosting verification

The repository remains a plain static GitHub Pages site. Merging the reviewed branch into `main` is the deployment trigger; passing Site checks is separate from a successful Pages deployment. Preserve the existing custom domain, `.nojekyll`, verification HTML, `app-ads.txt` and Android asset associations.

GitHub Pages does not support arbitrary repository `.htaccess` or `_redirects` rules. The two aliases in `content/redirects.json` use zero-second meta refresh, a canonical link to the established article, `noindex, follow`, and a useful fallback link. Google documents an [immediate meta refresh as a permanent redirect signal](https://developers.google.com/search/docs/crawling-indexing/301-redirects). The static file still returns HTTP 200; this implementation is **not an HTTP 301/308**. If actual server responses are required for those aliases, use a configured edge/hosting redirect service, with each alias pointing directly to the established URL and no chain.

After deployment, inspect GitHub repository **Settings -> Pages** and verify the domain and [Enforce HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https). The current connector cannot access/configure this hosting setting, and external fetches do not expose a reliable response chain here. Do not claim enforcement has been changed or that every HTTP/www response is verified.

Verify response codes and Location headers for:

| Input | Expected final result |
| --- | --- |
| `http://nextflow-apps.com/articles/how-to-use-a-music-sleep-timer-on-android/` | Server-side permanent redirect to its HTTPS canonical |
| HTTP study guide | Server-side permanent redirect to its HTTPS canonical |
| HTTPS screen-off URL without trailing slash | Server-side redirect to the established trailing-slash URL |
| `www.nextflow-apps.com`, if DNS is configured | Canonical host, without a separately indexable copy |
| Both known typo aliases | Immediate direct canonical destination; note static fallback HTTP 200 |
| A genuinely missing nested route | HTTP 404 with the custom recovery page, noindex, no canonical |
| Canonical screen-off, sleep, Noctra and campaign URLs | HTTP 200, correct canonical, no noindex |

A normal local Python server automatically redirects directory slash variants, and the browser tests simulate GitHub Pages' custom 404 serving. These checks exercise the code; they do not prove production hosting response headers. Use browser Network tools or `curl -I` / `curl -IL --max-redirs 5` against deployed URLs to verify the actual hosting configuration. If `www` is not configured, inspect DNS before enabling it. Keep every indexable internal link on the canonical host/path.

## Search Console actions after successful deployment

1. Save an export of the **same supplied baseline period**, if available, including page/query, device, country, search type and average position. The original date range was not provided; record the actual deployment date separately.
2. Re-submit or revalidate `https://nextflow-apps.com/sitemap.xml` in the existing domain property. It contains the same 25 canonical indexable pages, no aliases or 404, with October 7 lastmod only for the materially updated home, library, nine guides, products, campaign and website privacy content.
3. Inspect and test the live screen-off URL, sleep-timer guide, HushFlow, NNN pillar, November Reset, Noctra and both Temvica guides/product. Confirm fetch success, rendered answer/CTA, self-canonical and crawlable CSS/JS. Request indexing for materially updated priorities after the live test succeeds; avoid repeated requests for unchanged legal pages.
4. Inspect the two typo URLs, non-slash screen-off URL, HTTP sleep/study URLs and `www` if relevant. Compare user-declared with Google-selected canonical. The selected canonical should converge on the established HTTPS URL; do not request indexing of aliases as new content.
5. Monitor Page indexing and duplicate/canonical exclusions. “Page with redirect” and consolidation exclusions can be expected for aliases; investigate any canonical product/article that becomes noindex, soft-404, blocked or chooses another canonical. There is no need to use the removals tool merely to consolidate normal aliases.
6. Watch the established winner's query families and position before interpreting CTR. For sleep-timer changes, compare CTR at similar positions/device/country/query composition, because a rank shift can change CTR independently of the title. Google may rewrite titles/snippets.
7. Review on day 7 for technical regressions, day 14 for early directional signals, and day 28 for comparable 28-day windows. These are review points, not promises of indexing or ranking within those dates. Segment November 2026 seasonality separately from evergreen traffic and compare the same days of week where possible.

## Baseline and post-deployment dashboard

Use the canonical page as the join key between Search Console and configured website-event reports. The supplied figures have no date range or position data and are not a complete traffic export.

| Page | Clicks | Impressions | Derived CTR |
| --- | ---: | ---: | ---: |
| Screen-off audio | 158 | 21,310 | 0.74% |
| Music sleep timer | 5 | 2,727 | 0.18% |
| Block distracting apps | 1 | 505 | 0.20% |
| Study Pomodoro | 1 | 379 | 0.26% |
| Noctra | 4 | 276 | 1.45% |
| Coding Pomodoro | 0 | 231 | 0% |
| NNN pillar | 4 | 112 | 3.57% |
| Homepage | 4 | 106 | 3.77% |
| Doomscrolling | 0 | 68 | 0% |
| HushFlow | 1 | 32 | 3.13% |
| Temvica | 0 | 26 | 0% |
| Article library | 1 | 25 | 4.00% |

Also record the supplied HTTP duplicates (159 sleep-timer impressions and 69 study impressions, zero clicks), support (one click / 38 impressions), and all other relevant pages from the full export. Do not add canonical and duplicate impressions together and assume they are unique people.

For **each important page**, compare impressions, clicks, CTR, average position, relevant query mix, article -> product actions, Play outbound clicks, primary CTA impressions/CTR and pricing interest. Split CTA positions, apps and campaign-vs-Play destinations. Use the formulas and consent limitations in [Acquisition measurement](acquisition-measurement.md).

Installs and paid conversions remain **unavailable** until verified app/Play attribution and billing reporting are connected. Website events alone cannot attribute an organic install, purchase or Lifetime upgrade. Record these fields as unavailable rather than zero. Establish a measured website-event baseline only after the collector is configured, and never compare instrumented counts to a pre-instrumentation zero.

Success means more qualified product-relevant traffic and measured actions without losing the current winner, followed by verified installs/purchases where attribution exists. Avoid fixed ranking/revenue promises or success claims based only on adding keywords.
