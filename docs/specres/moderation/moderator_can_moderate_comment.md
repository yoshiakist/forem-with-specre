---
id: "01KJ1733YCRFGKZZN1ZR6JBEHC"
name: "moderator_can_moderate_comment"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/moderations_controller.rb`
- `app/javascript/packs/commentModPage.js`
- `app/views/moderations/mod.html.erb` (Template)
- `spec/requests/moderations_spec.rb` (Test)

## Functional Overview

When a trusted user navigates to a comment's moderation page, the system verifies their authorization via Pundit (`Comment#moderate?` policy), loads the target comment by decoding its base-26 ID, and renders the shared moderation template. The page displays the comment's reaction buttons (thumbsup, thumbsdown, vomit) pre-populated with the moderator's existing reactions, along with a flag-user button targeting the comment author. The JavaScript layer manages mutually exclusive reactions — a positive vote clears any negative votes in the UI and vice versa — and POSTs each reaction toggle to `/reactions`, updating button state based on whether the server reports a `create` or `destroy` outcome. Admins additionally see links to the comment admin panel and the author's user admin page, and a delete button that requires a confirmation dialog before submitting.

## Design Intent

The comment action reuses the shared `moderations/mod` template rather than having a dedicated template. The template branches on `@moderatable.class.name` to conditionally show comment-only controls (admin delete button, admin navigation links) while suppressing article-only controls (tag adjustment form, experience level rating). This avoids duplicating the common reaction UI while keeping comment-specific behavior isolated.

The base-26 decoding of `params[:id_code]` matches the URL scheme used throughout the application for comment permalinks, ensuring the moderation route is consistent with how comments are addressed elsewhere.

## Scenarios

### Trusted user opens a comment moderation page

1. A trusted user requests the moderation page for a specific comment (e.g., `GET /username/comment/:id_code/mod`).
2. The system checks `Comment#moderate?` via Pundit; the user is authorized.
3. The comment is loaded by converting the base-26 `id_code` to an integer and finding the matching `Comment` record.
4. The shared moderation template is rendered, displaying reaction buttons with the moderator's previously cast reactions pre-highlighted, a flag-user button for the comment author, and — for admins — links to the comment admin page and user admin page.

### Moderator toggles a reaction on a comment

1. The moderator clicks a reaction button (thumbsup, thumbsdown, or vomit) on the comment moderation page.
2. The frontend POSTs to `/reactions` with the `reactable_type`, `category`, and `reactable_id` from the button's data attributes.
3. If the server responds with `result: "create"`, the clicked button receives the `reacted` class and any contradictory reactions are visually cleared (thumbsup clears thumbsdown and vomit; any negative vote clears thumbsup).
4. If the server responds with `result: "destroy"`, the `reacted` class is removed from the clicked button, toggling the reaction off.
5. If the server returns an error, an alert is displayed to the moderator.

### Admin deletes a comment from the moderation page

1. An admin views the moderation page for a comment that has not already been deleted.
2. A delete button is shown in a secondary card panel.
3. The admin clicks the delete button; a browser confirmation dialog asks "Are you SURE you want to delete this comment?".
4. If the admin confirms, the form submits a `PATCH` request to `comment_admin_delete_path` for the comment.
5. If the admin cancels, the form submission is suppressed and the page remains unchanged.

### Unauthenticated or untrusted user attempts to access comment moderation

1. A user who is not signed in, or who lacks the trusted role, requests a comment moderation URL.
2. Pundit raises `Pundit::NotAuthorizedError` because the `Comment#moderate?` policy is not satisfied.
3. The application renders a 404 Not Found response, revealing nothing about the existence of the page.

## Failures / Exceptions

- If the `id_code` parameter does not correspond to any `Comment` record, `Comment.find` raises `ActiveRecord::RecordNotFound`, resulting in a 404 response.
- If the fetch call to `/reactions` fails at the network level (no response), the frontend catches the error and displays an alert with the error details.
