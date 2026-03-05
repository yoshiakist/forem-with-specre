---
id: "01KJXXWWYZMY0J3Y74HP34NJGC"
name: "user_can_dismiss_hero_campaign_banner"
status: "draft"
---

## Related Files

- `app/javascript/packs/heroBannerClose.js`

## Functional Overview

When the hero campaign banner is present on the page, a close icon is rendered alongside it. Clicking the close icon hides the banner immediately and records the banner's name in `localStorage` so the dismissal can be persisted across page visits. The close icon is also given an accessible `aria-label` at initialization time to describe its purpose to assistive technology users.

## Design Intent

Storing the dismissed banner name in `localStorage` (keyed as `exited_hero`) allows the server or client-side rendering logic to suppress the banner on subsequent page loads without requiring a server round-trip or cookie. Using the banner element's `data-name` attribute as the stored value lets a single generic script handle multiple distinct campaigns.

## Key Members

- `hero-html-wrapper` — ID of the banner container element; carries a `data-name` attribute identifying the current campaign
- `js-hero-banner__x` — ID of the close icon element that triggers dismissal
- `exited_hero` — `localStorage` key used to record the name of the dismissed campaign banner

## Scenarios

### User dismisses the banner

1. The page loads and both the banner wrapper (`#hero-html-wrapper`) and the close icon (`#js-hero-banner__x`) are present in the DOM.
2. The script sets `aria-label="Close campaign banner"` on the close icon so screen reader users understand its purpose.
3. The user clicks the close icon.
4. The campaign name (read from the banner wrapper's `data-name` attribute) is saved to `localStorage` under the key `exited_hero`.
5. The banner wrapper is hidden immediately by setting its display to `none`.

## Failures / Exceptions

- If either `#hero-html-wrapper` or `#js-hero-banner__x` is absent from the DOM, the script exits without error and no event listener is attached.
