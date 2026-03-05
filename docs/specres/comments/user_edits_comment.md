---
id: "01KJ5DYNF9N28R72J7M5FT4KVZ"
name: "user_edits_comment"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/comments_controller.rb`
- `app/models/comment.rb`
- `app/policies/comment_policy.rb`
- `spec/requests/comments_update_spec.rb` (Test)
- `spec/system/comments/user_edits_a_comment_spec.rb` (Test)
- `app/views/comments/edit.html.erb` (Template)
- `app/views/comments/_form.html.erb` (Template)

## Functional Overview

A signed-in user who authored a comment can edit its body markdown through an edit form. On submission, the system re-parses the markdown, stamps `edited_at` with the current time, updates any mention notifications, and re-renders the comment index view in place — without issuing an HTTP redirect — to avoid a race condition where a cached response could serve stale content before the cache is busted. If the markdown fails to parse, or any other error occurs, the edit form is re-rendered with an inline error message. Users who did not author the comment, or who are suspended or marked as spam, are denied access at the policy layer.

## Design Intent

The controller renders the index view directly after a successful update rather than redirecting. This is an intentional workaround for a cache race condition: a redirect would cause the browser to re-request a URL that may still be cached with pre-edit content, leading to stale data being shown. Rendering inline guarantees the fresh content is delivered in the same response.

## Key Members

- `edited_at` — timestamp set to the current time on every successful update; surfaced in the view as an "Edited on" label with an ISO 8601 `datetime` attribute
- `body_markdown` — the editable field; triggers markdown re-evaluation and mention re-processing on change
- `receive_notifications` — also permitted for update alongside `body_markdown`

## Scenarios

### Successful edit via the article page

1. The author visits an article page and opens the dropdown menu on their comment.
2. The author clicks "Edit", which opens the edit form pre-populated with the existing markdown.
3. The author modifies the text and submits the form.
4. The system re-parses the markdown, stamps `edited_at`, refreshes mention notifications, and returns the updated comment inline (HTTP 200, no redirect).
5. The page displays the updated text and an "Edited on" label with a valid ISO 8601 timestamp.

### Successful edit via the comment permalink

1. The author navigates directly to the comment's permalink.
2. The author opens the dropdown, clicks "Edit", and modifies the text.
3. On submission, the system processes the edit the same way and renders the updated comment inline.
4. A "Dismiss" link is available on the edit form when accessed via permalink.

### Non-author or suspended user attempts to edit

1. A user who did not author the comment, or whose account is suspended or flagged as spam, requests the edit form for that comment.
2. The policy denies the action; the system responds with an authorization error and does not expose the edit form.

### Markdown parsing error during update

1. The author submits a body that causes the markdown renderer to raise a parsing error.
2. The system catches the error, sets a flash error message describing the problem, and re-renders the edit form without saving any changes.

## Failures / Exceptions

- **Markdown parsing error (`ContentRenderer::ContentParsingError`):** The renderer raises during `evaluate_markdown`. The error is added to the model and surfaced via `flash.now[:error]`; the edit form is re-rendered.
- **Unexpected runtime error (`StandardError`):** Any other exception during update is caught, the error message is placed in `flash.now[:error]`, and the edit form is re-rendered.
- **Unauthorized access:** `comment_policy#edit?` returns `false` for non-authors and for users who are spam or suspended, causing Pundit to raise an authorization error before the edit form or update is processed.
