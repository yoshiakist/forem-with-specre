---
id: "01KJ16Z3Y34HEH2GSWHHXW3NAM"
name: "moderator_can_moderate_article_content"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/moderations_controller.rb`
- `app/helpers/moderations/actions_panel_helper.rb`
- `app/javascript/actionsPanel/actionsPanel.js`
- `app/javascript/actionsPanel/initializeActionsPanelToggle.js`
- `app/javascript/packs/actionsPanel.js`
- `app/javascript/packs/articleModerationTools.js`
- `app/javascript/utilities/moderation.js`
- `app/errors/moderation_unauthorized_error.rb`
- `app/views/moderations/mod.html.erb` (Template)
- `app/views/moderations/actions_panel.html.erb` (Template)
- `app/views/admin/users/show/overview/_tag_moderation.html.erb` (Template)
- `spec/requests/moderations_spec.rb` (Test)
- `spec/helpers/moderations/actions_panel_helper_spec.rb` (Test)
- `app/javascript/utilities/__tests__/moderation.test.js` (Test)

## Functional Overview

When a trusted user or tag moderator navigates to an article's moderation view (`GET /:username/:slug/mod` or the floating actions panel at `GET /:username/:slug/actions_panel`), the system authorizes them via Pundit's `Article#moderate?` policy, loads the article by slug, and builds the moderation context including the moderator's tag roles, allowed adjustments, and any existing vomit reactions against the author. The floating actions panel is rendered inside an iframe injected into the article show page by `articleModerationTools.js`, which gates panel initialization behind a `js-policy-article-moderate` DOM policy check. Inside the panel, moderators can cast quality reactions (thumbsup, thumbsdown, vomit), adjust article tags by posting to `/tag_adjustments`, rate the article's experience level by posting to `/rating_votes`, and (if authorized) toggle the article's featured status via `PATCH /articles/:id/admin_featured_toggle`. The `ActionsPanelHelper#last_adjusted_by_admin?` helper prevents tag moderators from reversing a tag adjustment that was last committed by an admin.

## Scenarios

### Trusted user opens the article moderation page

1. A trusted user navigates to `GET /:username/:slug/mod`.
2. The `article` action calls `load_article`, which runs `authorize(Article, :moderate?)` via Pundit; non-trusted users receive a 404.
3. The controller loads the article by slug, collects the moderator's tag roles, and sets `@allowed_to_adjust` based on whether the user is a super admin or holds any tag moderator roles.
4. The `moderations/mod` template is rendered, showing reaction buttons and, conditionally, a tag adjustment form and experience-level rating buttons.

### Moderator opens the floating actions panel on an article page

1. On page load, `articleModerationTools.js` checks whether the current user's policies include `js-policy-article-moderate` with `visible: true`.
2. If authorized, `initializeActionsPanel` from `initializeActionsPanelToggle.js` injects an iframe pointing to `/:username/:slug/actions_panel` and wires a toggle button (suppressed on the `/mod` center page via `isModerationPage`).
3. The `actions_panel` controller action calls `load_article` (same authorization path), checks whether the moderator has previously flagged the author, and renders `moderations/actions_panel` with the `is_mod_center` local variable.
4. Inside the iframe, `actionsPanel.js` is loaded by the `actionsPanel` pack and calls `initializeActionsPanel`, which sets up reaction buttons, tag adjustment listeners, experience-level listeners, and the feature-article button.

### Moderator adjusts a tag on an article

1. The moderator expands the "Adjust tags" dropdown (only visible when the `allow_tag_adjustment?` policy is satisfied).
2. To remove a tag, the moderator clicks the tag button; `handleRemoveTagButton` reveals a reason textarea and confirm button.
3. To add a tag, an admin clicks "Add tag" or a tag moderator clicks one of their own managed tags; `handleAddModTagButton` or `handleAddTagButtonListeners` reveals the corresponding input and reason fields.
4. On confirm, `adjustTag` posts to `POST /tag_adjustments` with `tag_adjustment.adjustment_type` set to `"removal"` or `"addition"` and a required reason.
5. On success, the tag is added to or removed from the article tag list in the DOM, a snackbar confirmation is shown, and the panel reloads. On failure, a snackbar error is displayed.
6. The `last_adjusted_by_admin?` helper prevents a tag moderator from adjusting a tag that was last committed by an admin, displaying a restriction notice instead.

### Moderator rates article experience level

1. The moderator expands the "Set experience level" dropdown.
2. Clicking a level button calls `updateExperienceLevel` with the user's ID, article ID, rating value, and `"experience_level"` group.
3. The function posts to `POST /rating_votes` with the rating payload. On success, the selected button receives the `selected` class and all others are cleared. On failure, an alert is shown.

### Admin features or unfeatures an article

1. An admin with `toggle_featured_status?` policy sees a feature/unfeature button in the actions panel.
2. Clicking the button calls `adminFeatureArticle` with the article ID and current featured state.
3. The function sends `PATCH /articles/:id/admin_featured_toggle` toggling the `article.featured` value between 0 and 1.
4. On success, the page redirects to the article path returned in the response. On failure, a snackbar error is displayed.

## Failures / Exceptions

- Unauthenticated requests or requests from non-trusted users to `/mod`, `/actions_panel`, or comment moderation paths raise `Pundit::NotAuthorizedError`, which the application translates to a 404 response.
- `ModerationUnauthorizedError` (a `StandardError` subclass) is defined for signaling unauthorized moderation attempts outside of the Pundit flow.
- If the article slug does not match any article, `load_article` calls `not_found` to render a 404.
- Tag adjustment network failures surface via a snackbar error message in the actions panel. JavaScript-level exceptions fall back to a native `alert`.
- Experience-level rating failures (`outcome.result !== 'Success'`) show the server error via a native `alert`.
- Article featuring failures show a snackbar error; network exceptions also show a snackbar rather than a native alert.
