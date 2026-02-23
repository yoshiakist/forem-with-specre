---
id: "01KJ5E25AA2Q7QPV35S0JZBJS2"
name: "moderator_posts_templated_comment"
status: "draft"
---

## Related Files

- `app/controllers/comments_controller.rb` (Source)
- `app/models/comment.rb` (Source)
- `app/policies/comment_policy.rb` (Source)

## Functional Overview

When a moderator invokes the `moderator_create` action, the system looks up a pre-defined response template by ID and verifies that the requesting user is authorized to use it for moderator comments. The comment is then created on behalf of the platform's mascot user rather than the human moderator, with the template's content as the body. On success, new-comment notifications are dispatched and any @mentions in the body are processed. If an identical comment already exists on the same commentable thread, the request is rejected with a conflict status. The action is always recorded in the audit log regardless of outcome.

## Design Intent

- **Mascot user as author:** Templated moderator comments are posted under a shared mascot account rather than the individual moderator's identity. This keeps the moderation voice consistent and avoids exposing which staff member responded.
- **Response template indirection:** By requiring a pre-approved `ResponseTemplate` rather than free-form text, the system limits what moderators can post through this path to vetted, editorially approved language.
- **Policy-gated template use:** The `use_template_for_moderator_comment?` policy check ensures that only users with moderator response-template access can trigger this path, keeping the authorization surface narrow.
- **Audit logging:** Every call to this action (success or failure) is written to the moderator audit log, providing an accountable trail of who triggered which action and when.

## Key Members

- `ResponseTemplate#content` — the pre-approved body text that becomes the comment body.
- `Settings::General.mascot_user_id` — the ID of the platform mascot account that appears as the comment author.
- `Comment#body_markdown` — populated from the response template content before saving.
- `permitted_attributes_for_moderator_create` — limits writable attributes to `commentable_id`, `commentable_type`, and `parent_id`; moderators cannot set body text directly.

## Scenarios

### Successful templated comment

1. A trusted moderator selects a response template from the moderation UI and submits it against a commentable resource (e.g., an article or a parent comment).
2. The system verifies the moderator is authorized to use mod-response templates and that the comment attributes are within the allowed set.
3. The system finds the mascot user and builds a new comment attributed to that user, with the template's approved text as the body.
4. The comment is saved; new-comment notifications are sent to relevant subscribers, and any @mentions in the template body are resolved and notified.
5. The moderator receives a success response containing the path to the newly created comment.

### Duplicate comment rejected

1. A moderator submits a response template for a commentable thread where an identical comment (same body, same parent ancestry) already exists.
2. The save fails due to a uniqueness constraint, but the system detects the existing duplicate record.
3. The system responds with HTTP 409 Conflict and a localized failure message; no new comment is created and no notifications are sent.

### Unauthorized or error path

1. A user without moderator response-template access attempts to reach the `moderator_create` endpoint.
2. The policy check raises an authorization error; the action skips the normal authorization flow and returns HTTP 422 with an error message.
3. The audit log still records the attempt because the `after_action` callback fires regardless of success or failure.

## Failures / Exceptions

- **Unauthorized user:** A non-moderator (or a moderator without template access) is rejected by `use_template_for_moderator_comment?` or `authorize @comment`. The request returns HTTP 422 and the `skip_authorization` rescue path records the failure.
- **Duplicate comment:** If the exact same body markdown already exists in the same ancestry thread, the system returns HTTP 409 Conflict rather than creating a second identical comment.
- **Unexpected errors:** Any `StandardError` raised during comment construction or saving is caught, authorization is skipped to prevent double-render, and the caller receives HTTP 422 with a localized error description.
- **Rate limiting:** If the moderator exceeds the `comment_creation` rate limit, the action returns early with no comment created and no audit event generated.
