---
id: "01KJ7H6SJ6Y6A8ENZAX9H1TR5G"
name: "system_validates_response_template_attributes"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/response_template.rb`
- `spec/models/response_template_spec.rb` (Test)
- `spec/policies/response_template_policy_spec.rb` (Test)

## Functional Overview

When a `ResponseTemplate` record is saved, the system enforces a set of attribute-level validations that ensure every template is internally consistent. The validations check that required fields are present and drawn from permitted enumerations, that the `content_type` is appropriate for the chosen `type_of` (e.g., comment types require `body_markdown`, email types require `plain_text` or `html`), that system-level template types are never associated with a user, and that ordinary (non-trusted) users cannot accumulate more than 30 personal templates.

## Key Members

- `TYPE_OF_TYPES` — exhaustive list of permitted `type_of` values: `personal_comment`, `mod_comment`, `abuse_report_email_reply`, `email_reply`, `tag_adjustment`.
- `USER_NIL_TYPE_OF_TYPES` — subset of `TYPE_OF_TYPES` that must have a `nil` user: `mod_comment`, `abuse_report_email_reply`, `email_reply`, `tag_adjustment`.
- `CONTENT_TYPES` — all permitted `content_type` values: `plain_text`, `html`, `body_markdown`.
- `COMMENT_CONTENT_TYPE` — single-element list `[body_markdown]`; required when `type_of` contains `"comment"`.
- `EMAIL_CONTENT_TYPES` — `[plain_text, html]`; required when `type_of` contains `"email"`.
- `user_nil_only_for_user_nil_types` — custom validation that rejects a `user_id` when `type_of` belongs to `USER_NIL_TYPE_OF_TYPES`.
- `template_count` — custom validation that caps personal templates at 30 for ordinary users; trusted users are exempt.

## Scenarios

### Valid attributes are accepted

1. A caller provides a template with `type_of`, `content_type`, `content`, and `title` all present and within permitted values.
2. The content uniqueness constraint (scoped to `user_id`, `type_of`, and `content_type`) is satisfied.
3. The system saves the record without errors.

### Comment type requires body_markdown content type

1. A template is submitted with a `type_of` that contains the word `"comment"` (e.g., `personal_comment` or `mod_comment`).
2. The system checks that `content_type` is `body_markdown`.
3. If any other `content_type` (such as `html`) is supplied, the system adds a validation error to `content_type` with the localized `comment_markdown` message and rejects the record.

### Email type requires plain_text or html content type

1. A template is submitted with a `type_of` that contains the word `"email"` (e.g., `email_reply` or `abuse_report_email_reply`).
2. The system checks that `content_type` is either `plain_text` or `html`.
3. If `body_markdown` or any other value is supplied, the system adds a validation error to `content_type` with the localized `email_text` message and rejects the record.

### System-level types reject a user association

1. A template is submitted with a `type_of` belonging to `USER_NIL_TYPE_OF_TYPES` (e.g., `mod_comment`, `email_reply`).
2. A non-nil `user_id` is provided.
3. The system adds a validation error to `type_of` with the localized `user_nil_only` message and rejects the record.

### Template count caps ordinary users at 30

1. An ordinary (non-trusted) user already has 30 response templates.
2. The user attempts to save a 31st template.
3. The system adds a validation error to `user` with the localized `limit_reached` message and rejects the record.
4. When the same user is granted the `trusted` role, the limit no longer applies and additional templates can be saved successfully.

## Failures / Exceptions

- Missing required field (`type_of`, `content_type`, `content`, or `title`): record is invalid with a presence error.
- `type_of` value not in `TYPE_OF_TYPES`: invalid with an inclusion error.
- `content_type` value not in `CONTENT_TYPES`: invalid with an inclusion error.
- Duplicate content for the same `user_id`, `type_of`, and `content_type` combination: invalid with a uniqueness error.
- Comment `type_of` paired with non-`body_markdown` content type: invalid with the `comment_markdown` localized message on `content_type`.
- Email `type_of` paired with `body_markdown` content type: invalid with the `email_text` localized message on `content_type`.
- `USER_NIL_TYPE_OF_TYPES` template submitted with a `user_id`: invalid with the `user_nil_only` localized message on `type_of`.
- Ordinary user exceeding the 30-template limit: invalid with the `limit_reached` localized message on `user`.
