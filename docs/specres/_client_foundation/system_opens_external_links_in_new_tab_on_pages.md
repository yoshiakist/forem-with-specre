---
id: "01KJXY245DK9WXSB7WC8PH3CNP"
name: "system_opens_external_links_in_new_tab_on_pages"
status: "draft"
---

## Related Files

- `app/javascript/packs/pageFunctionality.js`

## Functional Overview

When a page finishes loading, the system scans all anchor elements with an `href` attribute inside the `#page-content` container and identifies any that point to an absolute URL on a different domain. For each such external link, the system sets `target="_blank"` so the browser opens it in a new tab, and ensures `rel` contains both `noopener` and `noreferrer` to prevent the opened page from accessing the opener and to avoid referrer leakage. Existing `rel` values on the link are preserved and merged with these two required values, avoiding duplicates.

## Design Intent

Opening external links in a new tab keeps users on the current page while allowing them to explore off-site content. Adding `noopener` and `noreferrer` is a security best practice that prevents the newly opened page from navigating the opener via `window.opener` and avoids sending HTTP `Referer` headers to external origins. The merge strategy ensures that any `rel` values set elsewhere (e.g., `sponsored`, `ugc`) are not overwritten.

## Key Members

- `backfillLinkTarget()` — scans `#page-content` for all `<a href>` elements and applies `target` and `rel` attributes to external links
- `appDomain` — the current page's `hostname`, used to distinguish internal from external URLs
- `newRelValues` — the required values `["noopener", "noreferrer"]` applied to every external link

## Scenarios

### External link with no existing rel attribute

1. The DOM finishes loading and `DOMContentLoaded` fires.
2. The system queries all `<a href>` elements inside `#page-content`.
3. For a link whose `href` starts with `http://` or `https://` and does not include the current hostname, the system sets `target="_blank"`.
4. Because the link has no existing `rel` attribute, the system sets `rel="noopener noreferrer"`.

### External link with an existing rel attribute

1. The DOM finishes loading and `DOMContentLoaded` fires.
2. The system finds an external link that already has a `rel` attribute (e.g., `rel="sponsored"`).
3. The system splits the existing value by spaces and merges it with `["noopener", "noreferrer"]`, deduplicating.
4. The system sets `target="_blank"` and writes the merged value back to `rel` (e.g., `rel="sponsored noopener noreferrer"`).

### Internal link is skipped

1. The DOM finishes loading and `DOMContentLoaded` fires.
2. The system finds a link whose `href` contains the current hostname.
3. The system makes no changes to `target` or `rel` for this link.

### Relative or non-HTTP link is skipped

1. The DOM finishes loading and `DOMContentLoaded` fires.
2. The system finds a link whose `href` does not start with `http://` or `https://` (e.g., a relative path or `mailto:` link).
3. The system makes no changes to `target` or `rel` for this link.

## Failures / Exceptions

- If `#page-content` does not exist in the DOM, `document.getElementById('page-content')` returns `null` and calling `querySelectorAll` on it will throw a `TypeError`. The function does not guard against this case.
