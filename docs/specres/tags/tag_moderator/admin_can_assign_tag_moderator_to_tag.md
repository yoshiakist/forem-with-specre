---
id: "01KJ405PD1DE1M82CXWR67V9TT"
name: "admin_can_assign_tag_moderator_to_tag"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/tags/moderators_controller.rb`
- `app/services/tag_moderators/add.rb`
- `app/services/tag_moderators/add_trusted_role.rb`
- `app/views/fields/tag_moderators_field/_form.html.erb` (Template)
- `app/views/fields/tag_moderators_field/_index.html.erb` (Template)
- `app/views/fields/tag_moderators_field/_show.html.erb` (Template)
- `app/views/mailers/notify_mailer/tag_moderator_confirmation_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/tag_moderator_confirmation_email.text.erb` (Template)
- `spec/services/tag_moderators/add_spec.rb` (Test)
- `spec/services/tag_moderators/add_trusted_role_spec.rb` (Test)
- `spec/requests/admin/tags/moderators_spec.rb` (Test)

## Functional Overview

An admin can assign a tag moderator role to a user by submitting a username via `POST /admin/content_manager/tags/:id/moderator`. The controller looks up the user by username and delegates to `TagModerators::Add`, which enables the tag mod newsletter setting, grants the `:tag_moderator` role scoped to the given tag, marks the tag as supported if it was not already, and sends a confirmation email to the new moderator. As a side effect, `TagModerators::AddTrustedRole` is called to elevate the user to the `:trusted` role unless they are already trusted or are spam/suspended, and optionally subscribes them to the community moderators newsletter. If Mailchimp is configured, both the tag moderators list and the community moderators list are managed via `Mailchimp::Bot`. All create and destroy actions are logged via `Audit::Logger`.

## Design Intent

The assignment flow is split across two service objects — `TagModerators::Add` for tag-specific concerns and `TagModerators::AddTrustedRole` for the cross-cutting trusted-role grant — so that the trusted-role promotion logic can be reused independently. Newsletter subscription is gated on Mailchimp settings being present, keeping the core behavior functional without a Mailchimp integration.

## Key Members

- `user_id` — ID of the user being promoted to tag moderator
- `tag_id` — ID of the tag the user will moderate
- `Result` — a value object returned by `TagModerators::Add` with `success?` and `errors` fields

## Scenarios

### Successful assignment

1. An admin submits a username and a tag ID to `POST /admin/content_manager/tags/:id/moderator`.
2. The controller resolves the username to a user record.
3. `TagModerators::Add` is called with the user ID and tag ID.
4. The user's `email_tag_mod_newsletter` notification setting is enabled.
5. The `:tag_moderator` role is granted to the user, scoped to the tag.
6. If the tag was not yet marked as supported, it is updated to supported.
7. `TagModerators::AddTrustedRole` is called, granting the `:trusted` role if the user does not already have it and is not spam/suspended. The `email_community_mod_newsletter` setting is also enabled.
8. A confirmation email is sent to the new moderator via `NotifyMailer#tag_moderator_confirmation_email`.
9. The admin is redirected back to the tag's edit page with a success flash message.
10. The action is logged via `Audit::Logger`.

### User not found by username

1. An admin submits a username that does not match any user record.
2. The controller sets an error flash message indicating the username was not found.
3. The admin is redirected back to the tag's edit page without any role changes.

### Assignment fails due to notification setting update error

1. An admin submits a valid username and tag ID.
2. The user is found, but updating the `email_tag_mod_newsletter` notification setting fails.
3. `TagModerators::Add` returns a result with `success?` false and the validation errors.
4. The controller sets an error flash message including the errors.
5. The admin is redirected back to the tag's edit page without any role changes.

## Failures / Exceptions

- If the username does not match any user, the request short-circuits with an error flash before calling any service.
- If the notification setting update fails inside `TagModerators::Add`, no role is granted and no email is sent; the failure is surfaced as an error flash to the admin.
- `TagModerators::AddTrustedRole` silently skips granting the trusted role if the user is already trusted or is spam/suspended.
