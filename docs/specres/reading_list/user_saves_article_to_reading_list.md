---
id: "01KJY0ZNYVV7A0AXPSJ5FXYN32"
name: "user_saves_article_to_reading_list"
status: "draft"
---

## Related Files

- `app/assets/javascripts/initializers/initializeReadingListIcons.js`

## Functional Overview

When a page loads, the reading list initializer queries all bookmark buttons and highlights those whose article IDs appear in the current user's `reading_list_ids`, then populates any reading-list count badges on the home page. When a user clicks a bookmark button, the handler prevents default navigation, sends an authenticated `readinglist` reaction request to the server, and on success updates the button's selected state and increments or decrements the sidebar count badge. Unauthenticated users are redirected to the login modal instead of submitting the request.

## Design Intent

An optimistic UI update is applied immediately on click (always showing the button as "saved") before the server response arrives, keeping the interaction feel instant. The actual server response then reconciles the true state, toggling the button back if the article was already in the list. This one-way optimistic strategy is explicitly noted in the source as intentional ("optimistic create only for now").

## Key Members

- `user.reading_list_ids` — array of article IDs already saved to the current user's reading list, stored in the `userData()` cookie/session object
- `button.dataset.reactableId` — the article ID associated with each bookmark button element
- `.bookmark-button` — CSS selector identifying all saveable bookmark buttons on the page
- `.js-reading-list-count` — CSS selector for sidebar/home-page count badge elements
- `category: 'readinglist'` — the reaction category value sent to the server when saving or unsaving

## Scenarios

### Page load — highlight already-saved articles

1. The page initializes and calls the reading list initializer.
2. All bookmark buttons (excluding those marked with `data-initial-feed`) are collected.
3. For each button, the current user's `reading_list_ids` are checked against the button's article ID.
4. If the article is already saved, the button receives the `selected` CSS class; otherwise the class is removed.
5. Every button registers a click listener for the save/unsave action.

### Page load — display reading list count badge

1. After buttons are initialized, any `.js-reading-list-count` elements on the page are located.
2. If the user has saved articles, each badge's inner text is set to the count; if the list is empty, the badge is cleared.
3. Each badge stores the current count in `data-count` for later incremental updates.

### Logged-in user saves an article

1. User clicks a bookmark button for an article not yet in their reading list.
2. The button is immediately rendered as selected (optimistic update).
3. A CSRF-protected `readinglist` reaction is posted to the server with the article's ID and type.
4. On a 200 response with `result: 'create'`, the button remains selected and the sidebar count badge increments by one.

### Logged-in user removes an article from the reading list

1. User clicks a bookmark button for an article already in their reading list.
2. The button is optimistically rendered as selected (no optimistic remove in this version).
3. A `readinglist` reaction request is sent; the server returns `result` other than `'create'`.
4. The button's `selected` class is removed, and the sidebar count badge decrements by one (unless the count is already zero).

### Unauthenticated user attempts to save an article

1. User clicks a bookmark button while not logged in.
2. The handler detects `data-user-status="logged-out"` on the document body.
3. A login modal is shown with `referring_source: 'post_index_toolbar'` and `trigger: 'reading_list'`.
4. No network request is made and the button state is unchanged.

## Failures / Exceptions

- Network or server errors during the reaction request are caught but produce no visible feedback to the user (error handling is acknowledged as absent in the source).
