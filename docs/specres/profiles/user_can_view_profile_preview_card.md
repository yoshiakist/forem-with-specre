---
id: "01KHZ69T25SN7PPC7HH7ZPCZ2D"
name: "user_can_view_profile_preview_card"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/profile_preview_cards_controller.rb`
- `app/views/profile_preview_cards/show.html.erb`
- `app/views/shared/_profile_preview_card.html.erb`
- `app/views/shared/_profile_card_content.html.erb`
- `app/javascript/profilePreviewCards/MinimalProfilePreviewCard.jsx`
- `app/javascript/profilePreviewCards/UserMetadata.jsx`
- `app/javascript/packs/users/profilePage.js`
- `app/views/notifications/shared/_profile_pic.html.erb`
- `app/javascript/packs/asyncUserStatusCheck.js`
- `app/views/profile_preview_cards/show.json.jbuilder` (Template)
- `spec/requests/profile_preview_cards_spec.rb` (Test)

## Functional Overview

When a user hovers over or activates a profile trigger (e.g., a username link), a dropdown preview card is fetched and displayed showing a snapshot of that user's profile. The card is served by `ProfilePreviewCardsController#show` via `GET /profile_preview_cards/:id`, which loads the target user with their profile and settings, sets HTTP cache headers with surrogate keys, and responds with either an HTML partial or a JSON payload. The HTML response renders a branded dropdown containing the user's avatar, name, follow button, optional tag line, and metadata fields (email, location, join date, and dynamic header fields from the user's profile). The JSON response supplies the same data — including summary, location, created_at, card color, and conditionally the user's email — for client-side rendering by `MinimalProfilePreviewCard` and `UserMetadata` Preact components.

## Design Intent

The dual HTML/JSON response design allows the same endpoint to serve two rendering contexts: a server-rendered hover card embedded directly in page HTML, and a lightweight client-side card used within article bylines and notification areas. Cache headers with surrogate keys enable efficient CDN invalidation per user profile, keeping the preview card fresh without full-page recaching.

## Key Members

- `@user` — the `User` record loaded with `:profile` and `:setting` associations, identified by `params[:id]`
- `card_color` — a computed hex color derived from the user's brand colors using `Color::CompareHex#brightness(0.88)`, used for the card's top border accent
- `display_email_on_profile` — a user setting that controls whether the email field is included in the JSON response and shown in the HTML card
- `ui_attributes_for(area: :header)` — dynamically resolved profile header fields (e.g., Work, Education) surfaced in both the HTML and JSON representations

## Scenarios

### Viewing the HTML preview card (signed out or signed in)

1. A client requests `GET /profile_preview_cards/:id` with an HTML `Accept` header.
2. The controller loads the user by ID (with profile and setting) and sets cache-control and surrogate key headers.
3. The response renders the `_profile_preview_card` partial wrapped in a branded dropdown container styled with the user's computed card color.
4. Inside the card, the user's avatar, name, subscription icon (if applicable), and a follow button are displayed.
5. If the user has a tag line, it appears below the follow button truncated to 200 characters.
6. Metadata fields (email if opted in, location, dynamic header fields, join date) are listed below the tag line.

### Fetching profile data as JSON for client-side rendering

1. A client requests `GET /profile_preview_cards/:id` with a JSON `Accept` header (e.g., `as: :json`).
2. The controller loads the user and sets cache headers, then renders `show.json.jbuilder`.
3. The JSON response includes `summary`, `location`, `created_at` (ISO 8601 UTC), `card_color`, and up to three dynamic header fields.
4. The email field is included only if the user's `display_email_on_profile` setting is enabled.
5. The client-side `MinimalProfilePreviewCard` component renders the avatar, name, follow button, and an empty metadata container; `UserMetadata` populates the metadata details (email, work, location, education, join date) from the JSON payload.

### Requesting a non-existent user

1. A client requests `GET /profile_preview_cards/:id` with an unknown user ID.
2. The controller raises `ActiveRecord::RecordNotFound`, resulting in a 404 response.

## Failures / Exceptions

- Requesting a profile preview card for an unknown user ID raises `ActiveRecord::RecordNotFound` regardless of whether the client is signed in or out, and regardless of whether the request is HTML or JSON.
- Email is omitted from both HTML and JSON responses when the user's `display_email_on_profile` setting is `false`.
