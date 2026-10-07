# Acquisition measurement

## What is implemented

`assets/js/acquisition.js` runs once on each canonical page. It collects a maximum of 100 events in current-page memory, provides `window.NextFlowAnalytics.getEvents()` for inspection, and emits local `nextflow:analytics` events. It performs no network requests, sets no cookies, uses no persistent tracking storage, and creates no visitor/session identifier. Query strings, referrers, form values and arbitrary object fields are excluded from the event payload.

There is **no configured collector or aggregate dashboard**. This is a working instrumentation interface, not a claim that installs, purchases or organic attribution are already measured. The website privacy policy describes the current implementation.

| Event | Trigger | Useful context |
| --- | --- | --- |
| `acquisition_page_view` | One canonical page load | `source_page`, `page_type`, article slug where applicable |
| `app_cta_view` | An instrumented anchor is at least 50% visible, once per anchor per page | `app`, `cta_location`, `cta_action` identifying the corresponding click event |
| `article_app_cta_click` | An article's Play action | App, canonical article path/slug, mid/end/body location, destination |
| `article_product_click` | A guide's relevant product-page link | Same context, destination `product` |
| `product_google_play_click` | A product's Play link | App, product path, hero/body/product-visual location |
| `pricing_interest_click` | Free/Premium comparison link | App, source page and location |
| `november_reset_cta_click` | November campaign discovery or its Play action | Noctra, source page, location, destination `campaign` or `google_play` |

The product hero is identified by `cta_location=hero`; a second redundant `hero_google_play_click` event is unnecessary. Click and middle-button actions share duplicate suppression per anchor per page. Tracking never prevents navigation. Failed collectors are caught, so buttons still work.

`source_page` comes from the HTTPS canonical path, not the current query string. The bounded fields are `event`, `source_page`, `page_type`, `app`, `article_slug`, `cta_location`, `cta_action` on impressions and `destination` on clicks. No timestamp is generated locally; a configured collector can assign its receipt time. Event totals are page/anchor counts, **not unique people**.

## Connect a real collector

Choose an existing analytics service/account or a small first-party endpoint, define retention/access and consent behavior, and update the privacy disclosure to identify that service before activating it. Do not install a second collector if a configured service is later added. Load its library only under the applicable consent conditions; this adapter does not disable unrelated vendor scripts.

Use the optional adapter, rather than forwarding the local CustomEvent directly. `setAdapter()` alone does not activate forwarding. `setConsent(true)` enables future events only, and both Do Not Track and Global Privacy Control override that permission. Revocation immediately disables forwarding. There is no replay of events gathered before consent.

The integration should listen for `nextflow:analytics-ready` **before** the deferred acquisition script executes, so an already granted preference can be applied before its page-view event. For example, this provider-neutral helper connects your actual consent service and collector:

```js
function connectNextFlowCollector(forwardEvent, hasAnalyticsConsent) {
  function boot() {
    const analytics = window.NextFlowAnalytics;
    analytics.setAdapter(forwardEvent);
    analytics.setConsent(hasAnalyticsConsent() === true);
  }
  window.addEventListener('nextflow:analytics-ready', boot, { once: true });
  if (window.NextFlowAnalytics) boot();
  return (granted) => window.NextFlowAnalytics?.setConsent(granted === true);
}
// Call with the real collector callback and consent getter.
// Subscribe the returned function to consent changes and revocation.
```

For an existing, consent-controlled dataLayer integration, `forwardEvent` may push the sanitized event to that layer. Do not create an unconditional dataLayer listener or enable automatic query/form/referrer capture. Verify provider transport completion for same-tab campaign/product transitions; supported beacon transport can help, without delaying navigation. No incoming UTM parameters or unverified Play referrer parameters are copied into outbound links.

If consent is granted after initial page/anchor impressions, those impressions are intentionally not replayed. Calculate comparable CTA rates using page loads whose measurement was active from initialization; do not divide later-consent clicks by missing earlier impressions. If a future collector supports separate consent-cohort reporting, document that cohort explicitly.

## Reporting definitions

- **Search CTR:** Search Console clicks / impressions, by canonical page and query/device/country cohort.
- **Article -> product rate:** `article_product_click` / eligible measured article page loads. This is per-page action frequency, not a user conversion rate; do not add several link placements and call the sum unique visitors.
- **Primary CTA CTR:** Relevant primary click count / `app_cta_view` filtered to the same `source_page`, `app`, `cta_location` and `cta_action` equal to that click-event name. This separates the primary button's exposure from the secondary product-details link's exposure.
- **Product -> Play:** `product_google_play_click` / eligible measured product page loads. Report hero separately from other placements.
- **November funnel:** Separate campaign-destination clicks from Play-destination clicks using `destination`.
- **Install/purchase conversion:** Unavailable from website events alone. Use verified Play Console/app-side attribution and billing data only when configured. Never treat a Play click as an install or a purchase.

The current payload does **not** classify organic traffic: no referrer or campaign information is captured. Website click totals therefore cover all measured acquisition sources. Compare them with Search Console separately. A future consent-approved source classification may be added only with a defined minimal payload and privacy update; do not label all website Play clicks “organic installs.”

Google Play destinations are centralized in `content/acquisition.json`, and the sync/check scripts keep static links consistent. The Android repositories and Install Referrer support were not supplied, so no attribution capability or referrer parameter has been invented here.
