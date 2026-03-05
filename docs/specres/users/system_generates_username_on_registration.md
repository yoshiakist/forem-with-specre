---
id: "01KJBGSZYSK50Y48DDMGSB635P"
name: "system_generates_username_on_registration"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/users/username_generator.rb`
- `app/models/user.rb`
- `spec/services/users/username_generator_spec.rb` (Test)

## Functional Overview

When a new user is registered, the system automatically assigns a unique username through `Users::UsernameGenerator`. The generator attempts username candidates in priority order: first, usernames derived from the user's OAuth provider profiles are normalized (lowercased, stripped of special characters); if those are taken, suffixed variants with a random numeric suffix are tried; and as a last resort, three randomly generated 12-character lowercase strings are tried. The `User` model invokes the generator via a `before_validation` callback (`set_username`), which falls through to generation only when no username has already been set.

## Design Intent

The fallback chain (normalized → suffixed → random) maximizes the chance that a human-readable, provider-derived username is assigned while guaranteeing eventual uniqueness without raising an error. Injecting both the `detector` and `generator` dependencies makes the service fully testable without database access.

## Key Members

- `usernames`: the initial list of candidate strings (typically OAuth provider usernames) passed to the generator
- `detector`: a collaborator responding to `exists?(username)` used to check uniqueness; defaults to `CrossModelSlug`
- `generator`: a callable that produces a random username string; defaults to the internal `random_username` method

## Scenarios

### Username derived from OAuth provider profile

1. User registers via an OAuth provider (e.g., GitHub or Twitter) that supplies a username field.
2. The system collects the provider username and passes it to `UsernameGenerator`.
3. The generator normalizes the candidate by lowercasing and removing any characters outside `[a-z0-9_]`.
4. The system checks whether the normalized username already exists.
5. Because it is available, the system assigns it as the user's username.

### Username taken — suffix fallback

1. User registers with a provider username that, after normalization, is already taken.
2. The generator appends a random number (0–99) to the normalized stem to form a suffixed candidate.
3. The system checks the suffixed variant for availability.
4. Because the suffixed variant is available, the system assigns it.

### No valid provider username — random fallback

1. User registers without a provider username, or the supplied list contains only blank or non-string values.
2. The generator skips the normalized and suffixed candidate phases entirely.
3. The system generates up to three random 12-character lowercase strings and checks each for availability.
4. The first available random string is assigned as the username.

### All generation candidates exhausted

1. Every normalized candidate, every suffixed candidate, and all random candidates happen to be taken (possible in tests via a stubbed detector).
2. The generator returns `nil`.
3. The `User` model receives `nil` for the username, which will subsequently fail standard username presence/length validations.

## Failures / Exceptions

- If all candidate usernames are unavailable (normalized, suffixed, and all random attempts), the generator returns `nil` rather than raising an exception; the responsibility for handling this falls to the caller's validation layer.
