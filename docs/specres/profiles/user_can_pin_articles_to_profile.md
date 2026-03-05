---
id: "01KHZ69FHDF80CY6ZM4CR87C8M"
name: "user_can_pin_articles_to_profile"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/profile_pins_controller.rb`
- `app/models/profile_pin.rb`
- `spec/models/profile_pin_spec.rb` (Test)
- `spec/requests/profile_pins_spec.rb` (Test)

## Functional Overview

Authenticated users can pin up to five of their own articles to their profile. Pinning is performed via `POST /profile_pins` and each pin associates the current user's profile with a specific article. The system enforces that only the article's author may pin it, prevents duplicate pins of the same article, and caps the total number of pins per profile at five. Pins are removed via `PUT /profile_pins/:id`, which destroys the record on behalf of the current user. After any create or remove operation the user's profile edge cache is invalidated.

## Design Intent

The `PUT` action is used for removal rather than `DELETE` to work around browser/form limitations that make it difficult to issue true DELETE requests. The five-pin limit and author-only constraint are enforced at the model layer so they apply regardless of how the record is created. Deletion of the associated article bypasses model callbacks (`dependent: :delete_all`) because no cleanup logic is needed on the pin side.

## Key Members

- `pinnable_id` — the ID of the article being pinned; must belong to the current user
- `profile_id` / `profile_type` — polymorphic reference to the owning profile; currently restricted to `"User"`
- `pinnable_type` — polymorphic type of the pinnable; currently restricted to `"Article"`

## Scenarios

### User pins an article to their profile

1. The authenticated user submits a `POST /profile_pins` request with the target article's ID.
2. The system creates a `ProfilePin` record linking the user's profile to the article.
3. A success flash message is set and the user is redirected back (falling back to `/dashboard`).
4. The user's profile edge cache is invalidated.

### System rejects a pin when the article does not belong to the user

1. The authenticated user submits a `POST /profile_pins` request with an article ID that belongs to another author.
2. The `ProfilePin` model validation `pinnable_belongs_to_profile` fails.
3. The record is not saved; an error flash message is set and the user is redirected back.

### System rejects a duplicate pin

1. The authenticated user attempts to pin an article they have already pinned.
2. The uniqueness constraint on `pinnable_id` scoped to `profile_id`, `profile_type`, and `pinnable_type` fails.
3. The record is not saved; an error flash message is set and the user is redirected back.

### System enforces the five-pin limit

1. The authenticated user already has five articles pinned to their profile.
2. The user submits a `POST /profile_pins` request for a sixth article.
3. The `only_five_pins_per_profile` validation fails on create.
4. The record is not saved; an error flash message is set and the user is redirected back.

### User removes a pin from their profile

1. The authenticated user submits a `PUT /profile_pins/:id` request for an existing pin ID.
2. The system destroys the matching `ProfilePin` record scoped to the current user's pins.
3. A success flash message is set and the user is redirected back (falling back to `/dashboard`).
4. The user's profile edge cache is invalidated.

## Failures / Exceptions

- Attempting to pin an article owned by another user causes a validation error (`pin_unpermitted`).
- Pinning the same article twice causes a uniqueness validation error.
- Attempting to add a sixth pin causes a validation error (`only_five`).
- Unauthenticated requests to `create` or `update` are rejected by `authenticate_user!` before reaching the action.
