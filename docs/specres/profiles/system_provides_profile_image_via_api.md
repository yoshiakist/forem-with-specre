---
id: "01KHZ6GA12DBP0WCYVDFT4H5HE"
name: "system_provides_profile_image_via_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/concerns/api/profile_images_controller.rb`
- `app/controllers/api/v0/profile_images_controller.rb`
- `app/controllers/api/v1/profile_images_controller.rb`
- `app/views/api/v0/profile_images/show.json.jbuilder` (Template)
- `app/views/api/v1/profile_images/show.json.jbuilder` (Template)
- `spec/requests/api/v0/profile_images_spec.rb` (Test)
- `spec/requests/api/v1/profile_images_spec.rb` (Test)
- `spec/requests/api/v1/docs/profile_images_spec.rb` (Test)

## Functional Overview

The system exposes a read-only API endpoint `GET /api/profile_images/:username` available in both v0 and v1 API versions. Given a username, it resolves the owner as either a registered user or an organization, and returns a JSON object containing the owner type, a 640px profile image URL, and a 90px profile image URL. The shared logic lives in a `Concern` module (`Api::ProfileImagesController`) that both versioned controllers include, keeping the implementation DRY. If no matching registered user or organization is found for the given username, the endpoint responds with a 404 Not Found.

## Design Intent

The behavior is extracted into an `ActiveSupport::Concern` so that both v0 and v1 controllers share identical resolution logic without duplication. The lookup tries the user first and falls back to the organization, which means a username collision between a user and an organization would always resolve to the user. Only registered (non-invited) users are considered, which prevents invited-but-not-yet-active accounts from being discoverable through the API.

## Scenarios

### Returning a user's profile image

1. A client sends `GET /api/profile_images/:username` with the username of a registered user.
2. The system looks up a registered user with that username.
3. The system responds with HTTP 200 and a JSON object where `type_of` is `"profile_image"`, `image_of` is `"user"`, `profile_image` is the 640px image URL, and `profile_image_90` is the 90px image URL.

### Returning an organization's profile image

1. A client sends `GET /api/profile_images/:username` with the username of an organization.
2. No registered user with that username exists, so the system looks up an organization with that username.
3. The system responds with HTTP 200 and a JSON object where `type_of` is `"profile_image"`, `image_of` is `"organization"`, `profile_image` is the 640px image URL, and `profile_image_90` is the 90px image URL.

### Username not found

1. A client sends `GET /api/profile_images/:username` with a username that does not match any registered user or organization.
2. The system responds with HTTP 404 Not Found.

### Invited (unregistered) user is not discoverable

1. A client sends `GET /api/profile_images/:username` with the username of a user whose account is in an invited state.
2. The system's user lookup is restricted to registered users only, so the invited user is not found.
3. No organization with that username exists either, so the system responds with HTTP 404 Not Found.

## Failures / Exceptions

- If the username does not resolve to either a registered user or an organization, the controller calls `not_found`, returning HTTP 404.
- Invited users are excluded from the user lookup (`User.registered` scope), so their usernames yield a 404 even if the account exists.
