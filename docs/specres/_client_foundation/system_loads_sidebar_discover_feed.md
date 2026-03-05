---
id: "01KJXY201SHSNYJJCG16X9A5B7"
name: "system_loads_sidebar_discover_feed"
status: "draft"
---

## Related Files

- `app/javascript/packs/mainSidebar.js`

## Functional Overview

On page load, the system fetches a "discover" feed of articles from the `/stories/feed/` endpoint scoped to the current subforem domain. The fetched articles are rendered as a list of linked items inside the `#main-side-feed` container in the sidebar, each showing an optional cover image, a subforem logo, and the article title. If the `FeedTracker` utility is available, it is initialised on the sidebar feed container to record click and impression events. On every InstantClick navigation change, the system resets any hovered state on sidebar items and scrolls the feed container back to the top.

## Design Intent

Fetching the discover feed client-side after the initial page load keeps the server-side render fast and allows the sidebar to reflect per-subforem content without coupling the article-show page to a specific feed context. Delegating impression and click tracking to `FeedTracker` keeps analytics concerns out of the rendering logic. HTML-escaping article titles before injecting them into `innerHTML` prevents XSS from user-supplied content. The `escapeHtml` function uses a detached DOM element rather than a regex or library so that the browser's own parser is the source of truth for escaping.

## Key Members

- `rootDomain` — the hostname extracted from the `href` of `#root-subforem-link`; used to scope the feed request to the current subforem
- `feedContainer` — the `#main-side-feed` DOM element that receives the rendered feed HTML
- `articleId` — the `data-article-id` attribute of `#article-show-container`; used to mark the currently-viewed article as active in the sidebar
- `FeedTracker` — imported from `feedEvents.js`; wraps the feed container to track click and impression analytics
- `sidebarTracker` — instance of `FeedTracker` configured with `contextType: 'sidebar'` and `feedConfigId` taken from the first item in the response

## Scenarios

### Happy path: feed is fetched and rendered

1. The browser loads the page and the script reads the `href` attribute of `#root-subforem-link` to derive the current subforem domain.
2. The system sends a GET request to `/stories/feed/?page=1&type_of=discover&passed_domain=<rootDomain>` with `Accept: application/json` and same-origin credentials.
3. The server responds with a JSON array of article objects.
4. For each article, the system builds an anchor element containing an optional cover image (with lazy loading and correct aspect-ratio style), a subforem logo image, and the HTML-escaped article title.
5. The anchor for the article whose `id` matches the current page's `data-article-id` receives the `active` CSS class.
6. The assembled HTML is written to `#main-side-feed`.
7. If `FeedTracker` is defined, a new tracker is initialised on the feed container with `contextType: 'sidebar'` and the `feedConfigId` from the first article, then `init()` is called.
8. Click listeners are attached to every `<a>` inside `#main-side-bar` so that clicking any link removes the `hovered` class from all links and adds `not-hovered`.

### Page article is highlighted in the sidebar

1. The `#article-show-container` element is present on the page and carries a `data-article-id` attribute.
2. When building the feed HTML, the system compares each article's `id` against the stored `articleId`.
3. The matching article's anchor receives the `active` CSS class; all other anchors do not.

### No subforem domain is set

1. `#root-subforem-link` is absent or its `href` cannot be split into a domain segment.
2. `rootDomain` defaults to an empty string.
3. The fetch request is sent with `passed_domain=` (empty value); the server returns a generic discover feed.

### InstantClick navigation resets hover state

1. InstantClick fires a `change` event as the user navigates to a new page without a full reload.
2. The system selects all elements with class `crayons-side-nav__item hovered`, removes `hovered`, and adds `not-hovered` to each.
3. If the element `#root-feed-card` exists, its `scrollTop` is reset to `0`.

## Failures / Exceptions

- If the fetch request fails (network error or non-OK response), the error is caught and logged to `console.error`; the `#main-side-feed` container is left empty and no further processing occurs.
- If `#main-side-feed` is absent from the DOM, the system skips rendering and tracker initialisation silently.
- If the response array is empty, `feedContainer.innerHTML` is set to an empty string and the `FeedTracker` block is skipped because `data[0]` would be undefined.
