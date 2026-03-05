---
id: "01KJVGDWG6JSDZ2K61C9PXX65N"
name: "admin_can_create_community_bot"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/community_bots/create_bot.rb`
- `app/policies/community_bot_policy.rb`
- `spec/services/community_bots/create_bot_spec.rb` (Test)
- `spec/policies/community_bot_policy_spec.rb` (Test)

## Functional Overview

`CommunityBots::CreateBot` is a service object that provisions a new community bot user for a given subforem. It enforces authorization by allowing only admins, super moderators, and subforem moderators to create bots. When authorized, it generates a unique bot email address scoped to the subforem's domain, derives a username either from the caller-supplied value or from the bot's name, creates a `User` record with `type_of: :community_bot`, and immediately issues an API secret for the bot. The service returns itself as a result object exposing `success?`, `error_message`, `bot_user`, and `api_secret`, allowing callers to inspect the outcome without raising exceptions on expected failures.

## Design Intent

The service follows the command-object pattern (`.call` class method delegating to an instance) so that callers never need to instantiate the class directly. All guard checks (`subforem_exists?`, `authorized?`) return `false` and populate `@error_message` rather than raising, which keeps failure paths explicit and easy to test. A `StandardError` rescue at the top level of `call` prevents unexpected database or validation failures from propagating to callers.

## Key Members

- `subforem_id` — identifies the subforem the bot belongs to; used for email domain, authorization, and the bot's `onboarding_subforem_id`
- `name` — the display name of the bot; also used to derive the default email slug and username
- `created_by` — the `User` who is requesting bot creation; checked for admin/moderator privileges
- `username` (optional) — if supplied, the bot uses this as its base username (deduplicated with a timestamp if taken); otherwise a username is generated from `name`
- `profile_image` (optional) — reserved for future use; profile-image assignment is currently disabled in the service

## Scenarios

### Successful bot creation by an admin

1. An admin or super moderator calls the service with a valid subforem ID, a bot display name, and the requesting user.
2. The service verifies the subforem exists and confirms the requester holds admin or moderator rights.
3. A unique email address is generated using the bot name slug and current timestamp, scoped to the subforem's domain.
4. A `User` record is created with `type_of: community_bot`, pre-confirmed and registered, with the requesting user recorded as `invited_by`.
5. An API secret is created for the new bot user.
6. The service returns with `success?` true, exposing `bot_user` and `api_secret`.

### Bot creation with a custom username

1. A caller provides an optional `username` parameter alongside the required fields.
2. If the username is not already taken, it is used as-is.
3. If the username is already taken, a timestamp suffix is appended to ensure uniqueness.
4. The resulting username is stored on the bot user record.

### Bot creation with auto-generated username

1. No `username` parameter is provided.
2. The service derives a base username from the bot's `name` by parameterizing it and appending `_bot_<timestamp>`.
3. The resulting username is stored on the bot user record.

### Subforem moderator creates a bot

1. A user who is a moderator of the target subforem (but not a global admin) calls the service.
2. The authorization check passes for subforem-scoped moderators.
3. Bot creation proceeds identically to the admin path.

## Failures / Exceptions

- **Subforem not found** — if the given `subforem_id` does not correspond to an existing record, the service returns `success? false` with `error_message: "Subforem not found"`.
- **Unauthorized caller** — if the requesting user is neither an admin, super moderator, nor a moderator of the target subforem, the service returns `success? false` with `error_message: "Unauthorized to create bots for this subforem"`.
- **User creation failure** — if `User.create!` raises a `StandardError` (e.g., a validation error), the exception is caught and `error_message` is set to `"Failed to create bot: <original message>"`.
