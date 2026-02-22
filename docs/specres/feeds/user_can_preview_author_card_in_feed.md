---
id: "01KJ24JHMGN7PEYMPPQ31D9D2V"
name: "user_can_preview_author_card_in_feed"
status: "draft"
---

## Related Files

- `app/javascript/packs/feedPreviewCards.jsx`
- `app/javascript/previewCards/feedPreviewCards.jsx`

## Functional Overview

When a user hovers over or focuses on a story card's author trigger in the feed, the system lazily fetches author metadata from `/profile_preview_cards/:authorId` and renders a `UserMetadata` preview card into the DOM. Fetched metadata is cached in memory to avoid duplicate requests. The preview card is shown as a dropdown anchored to the trigger button; it repositions on scroll and is torn down on page navigation or unload. New story cards added to the feed dynamically (via DOM mutations) are automatically wired up with the same dropdown behavior.

## Design Intent

Lazy fetching on hover or focus avoids loading author metadata for all feed items upfront, which keeps initial page load lean. The in-memory cache (`cachedAuthorMetadata`) ensures that repeated hovers on the same author result in only one network request per page lifecycle.

## Key Members

- `cachedAuthorMetadata` — module-level object keyed by author ID; stores previously fetched metadata to prevent duplicate API calls
- `metadataPlaceholder.dataset.fetched` — flag set on the DOM element to prevent concurrent duplicate requests for the same placeholder

## Scenarios

### User hovers over an author trigger for the first time

1. The user moves the cursor over an element with class `profile-preview-card__trigger` inside the feed's `#main-content` area.
2. The system finds the sibling `author-preview-metadata-container` element within the trigger's parent.
3. Because neither the element's `data-fetched` flag nor an in-memory cache entry exists for the author, the system fetches metadata from `/profile_preview_cards/:authorId`.
4. The response is stored in the in-memory cache and the `UserMetadata` component is rendered into the placeholder element.
5. The dropdown's accent color is updated via a CSS custom property (`--card-color`) to match the author's card color.

### User hovers over the same author trigger a second time

1. The user triggers a `mouseover` event on the same `profile-preview-card__trigger` element again.
2. The `data-fetched` flag is already set on the `author-preview-metadata-container` element, so the function returns immediately without making another network request.

### User focuses on an author trigger via keyboard

1. The user navigates to a story card's author trigger using the keyboard, firing a `focusin` event on `#main-content`.
2. The same `checkForPreviewCardDetails` handler runs, finds the metadata placeholder, and fetches or uses cached metadata exactly as in the hover scenario.

### New story cards are added to the feed dynamically

1. The `MutationObserver` watching `#index-container` detects new child nodes added to the feed (e.g., via infinite scroll or live updates).
2. `initializeFeedPreviewCards` is called, which queries for `button[id^=story-author-preview-trigger]` elements that do not yet have `data-initialized` set.
3. Each new trigger is wired up with `initializeDropdown`, adding `onOpen` and `onClose` callbacks that toggle the `showing` class on the dropdown content element.

### Preview card dropdown repositions on scroll and is cleaned up on navigation

1. A scroll event listener is attached to `document` using `getDropdownRepositionListener` so the dropdown follows its anchor as the page scrolls.
2. When InstantClick fires a `change` event (page navigation) or the browser fires `beforeunload`, the `MutationObserver` is disconnected and the scroll listener is removed to prevent memory leaks.

## Failures / Exceptions

- If the `author-preview-metadata-container` element is not found inside the trigger's parent, no fetch is attempted and no error is raised; the hover/focus event is silently ignored.
- If `document.getElementById('index-container')` returns null, the `MutationObserver` is not started and no mutation observation occurs.
- If the dropdown element identified by `aria-controls` is not found in the DOM, the trigger is skipped and not initialized.
