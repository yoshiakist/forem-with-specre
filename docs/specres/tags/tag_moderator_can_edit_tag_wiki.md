---
id: "01KJ41WHZ0KRBSTTD55T6WPTM6"
name: "tag_moderator_can_edit_tag_wiki"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/tags_controller.rb`
- `app/policies/tag_policy.rb`
- `app/models/tag.rb`
- `app/views/tags/edit.html.erb` (Template)
- `spec/requests/tags_spec.rb` (Test)
- `spec/policies/tag_policy_spec.rb` (Test)
- `spec/system/tags/user_updates_a_tag_spec.rb` (Test)

## Functional Overview

Tag moderators and super admins can edit a tag's wiki content through the public `TagsController#edit` and `TagsController#update` actions. Access is gated by `TagPolicy#edit?`, which grants permission only to users who are a super admin or a moderator specifically assigned to the tag being edited. The edit form allows updating the tag's wiki body (in Markdown), rules, short summary, display name, and background color. On a successful save, the user is redirected back to the edit page with a success flash; on failure, the edit form is re-rendered with validation error messages.

## Design Intent

Authorization is scoped per-tag: a moderator of one tag cannot edit a different tag. This intentional scoping prevents moderator privilege escalation while still giving tag moderators full control over the content of their specific tag.

## Key Members

- `TAGS_ALLOWED_PARAMS`: the set of fields a moderator may submit — `wiki_body_markdown`, `rules_markdown`, `short_summary`, `pretty_name`, `bg_color_hex`, `text_color_hex`.
- `convert_empty_string_to_nil`: normalizes empty hex color strings to `nil` before saving, because empty strings fail hex color validations.

## Scenarios

### Authorized user loads the edit form

1. A user who is a super admin or a tag moderator for a given tag navigates to `/t/:tag/edit`.
2. The system looks up the tag by name and authorizes the current user via `TagPolicy#edit?`.
3. The edit form is rendered, showing the tag's current wiki body, rules, short summary, display name, and background color.
4. If the current user is also an admin, a link to the admin tag management panel is shown alongside the public edit form.

### Tag moderator successfully updates tag wiki content

1. The moderator submits the edit form with valid field values (e.g., updated wiki body Markdown or short summary).
2. The system permits the params, converts any empty hex color string to `nil`, and calls `Tag#update`.
3. Before saving, the model evaluates the Markdown fields into HTML via `MarkdownProcessor::Parser` and runs all validations.
4. The save succeeds; the user is redirected to `/t/:tag/edit` with a success flash message.

### Tag moderator submits invalid data

1. The moderator submits the edit form with an invalid value — for example, a hex color that does not match `HEX_COLOR_REGEXP`.
2. Validation fails on the `Tag` model; the update is rejected.
3. The controller re-renders the edit form with the error messages displayed in a danger notice.

### Unauthenticated or unauthorized user attempts to access the edit form

1. A user who is not signed in attempts to visit `/t/:tag/edit`.
2. The `authenticate_user!` before-action redirects them to the magic link sign-in page.
3. Alternatively, a signed-in user who is neither a super admin nor a tag moderator for the tag receives a `404 Not Found` response (Pundit raises `NotAuthorizedError`, which is handled as not found).

### Moderator of one tag attempts to edit a different tag

1. A user who holds the `tag_moderator` role for tag A attempts to access the edit form or submit an update for tag B.
2. `TagPolicy#edit?` checks `user.tag_moderator?(tag: record)` against tag B and returns `false`.
3. The request is rejected with a `404 Not Found` response.

## Failures / Exceptions

- Empty hex color values (`""`) submitted via the form are converted to `nil` before validation to avoid spurious format errors.
- If `Tag.find_by!(name: params[:tag])` finds no matching tag, Rails raises `ActiveRecord::RecordNotFound` and returns a 404 response.
