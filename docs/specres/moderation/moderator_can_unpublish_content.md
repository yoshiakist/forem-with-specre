---
id: "01KJ16Z3FNFCXTAK705DRJ0WVR"
name: "moderator_can_unpublish_content"
status: "draft"
---

## Related Files

- `app/javascript/packs/unpublishPostModal.jsx`
- `app/javascript/packs/modals/unpublishAllPosts.js`
- `app/views/moderations/modals/_unpublish_post_modal.html.erb` (Template)
- `app/views/moderations/modals/_unpublish_all_posts.html.erb` (Template)

## Functional Overview

Moderators and admins can unpublish a single article or all articles by a given user through confirmation modals rendered inside the moderation iframe. The single-post flow reads article metadata from the trigger element's dataset, displays a confirmation modal with author context, and on confirmation sends a PATCH request to `/articles/:id/admin_unpublish`, redirecting the top-level window to the returned path on success. The bulk-unpublish flow reads a user ID and an optional moderator note from the modal form, then sends a POST request to `/admin/member_manager/users/:id/unpublish_all_articles`. Both flows display a snackbar notification on error, cache the modal's HTML to prevent duplicate-ID conflicts when the Preact modal helper clones content, and close the modal window when the operation completes.

## Design Intent

Modal HTML is extracted from its hidden container and removed from the DOM on first use. This avoids duplicate HTML `id` attribute conflicts that would occur if the modal helper cloned content that still existed in the parent document.

## Key Members

- `articleId`, `authorUsername`, `articleSlug`, `modalContentSelector` — dataset attributes read from the trigger element to parameterize the single-post modal
- `userId`, `modalTitle`, `modalSize`, `modalContentSelector` — dataset attributes read from the trigger element to parameterize the bulk-unpublish modal
- `note.content` — optional moderator note text submitted alongside a bulk-unpublish request, entered in the `#note_content` textarea

## Scenarios

### Moderator unpublishes a single post

1. Moderator clicks an "Unpublish post" trigger element that carries `articleId`, `authorUsername`, `articleSlug`, and `modalContentSelector` as dataset attributes.
2. `toggleUnpublishPostModal` is called; it reads those attributes and calls `showWindowModal` in the parent document, injecting the cached modal HTML and setting the title to "Unpublish post".
3. On modal open, `activateModalUnpublishBtn` attaches a click listener to the `#confirm-unpublish-post-action` button.
4. Moderator clicks the destructive confirm button; `confirmAdminUnpublishPost` issues a PATCH request to `/articles/:id/admin_unpublish` with the article ID, username, and slug.
5. On success, `window.top.location` navigates to the path returned in the response, and the modal window closes.

### Moderator unpublishes all posts by a user

1. Moderator navigates to a user's admin page where a `#unpublish-all-posts-btn` element is present.
2. `toggleUnpublishAllPostsModal` reads `modalTitle`, `modalSize`, and `modalContentSelector` from the button's dataset and calls `showWindowModal` in the parent document.
3. On modal open, `activateUnpublishAllPostsBtn` attaches a click listener to the `#unpublish-all-posts-submit-btn` button.
4. Moderator optionally fills in the note textarea, then clicks the submit button.
5. `unpublishAllPosts` reads `userId` from the button's dataset and the note text from `#note_content`, then issues a POST request to `/admin/member_manager/users/:id/unpublish_all_articles` with both values.
6. The response message is displayed in a snackbar and the modal closes.

## Failures / Exceptions

- If the PATCH or POST request throws a network error, a snackbar with the error message is shown and the modal is closed.
- If the server returns a non-success `message` for a single-post unpublish, a snackbar prefixed with "Error:" is displayed instead of navigating.
- If the server returns a non-success response for a bulk unpublish, the outcome's `message` field is displayed in a snackbar (no redirect occurs).
