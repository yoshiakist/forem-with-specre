---
id: "01KHZ795DAZ7K0BZGY252PBQ10"
name: "user_can_suggest_a_podcast"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/podcasts_controller.rb`
- `app/models/podcast.rb`
- `app/models/podcast_ownership.rb`
- `app/views/podcasts/new.html.erb` (Template)
- `app/views/podcasts/_form.html.erb` (Template)
- `spec/requests/podcasts/podcast_create_spec.rb` (Test)
- `spec/requests/podcasts/podcast_show_spec.rb` (Test)
- `spec/models/podcast_spec.rb` (Test)
- `spec/models/podcast_ownership_spec.rb` (Test)
- `spec/system/podcasts/user_visits_podcast_page_spec.rb` (Test)

## Functional Overview

An authenticated user can suggest a new podcast by submitting a form at `POST /podcasts` with fields including title, feed URL, slug, main color hex, and an image. The system validates the submitted data — including image file type and filename length — and if valid, saves the podcast in an unpublished state and sets the submitting user as its creator. If the submitting user declares ownership via the `i_am_owner` flag, they are granted the `podcast_admin` role on the new podcast. Validation failures re-render the suggestion form with inline error messages.

## Design Intent

Podcasts are created in an unpublished state so that a platform administrator can review and approve them before they become visible. Ownership self-declaration at submission time immediately grants the declaring user admin rights, decoupling the editorial review step from the initial access grant.

## Key Members

- `PODCASTS_ALLOWED_PARAMS` — the set of permitted form fields: `title`, `feed_url`, `slug`, `main_color_hex`, `image`, `pattern_image`, `description`, `twitter_username`, `website_url`, `android_url`, `itunes_url`, `overcast_url`, `soundcloud_url`
- `i_am_owner` — checkbox param; when submitted as `"1"`, grants the `podcast_admin` role to the creator on the new podcast
- `Podcast#published` — defaults to `false` on creation; the podcast is not publicly visible until explicitly published

## Scenarios

### Authenticated user loads the suggestion form

1. A signed-in user navigates to `GET /podcasts/new`.
2. The system renders the suggestion form alongside a list of existing available podcasts.

### Unauthenticated user is redirected

1. A visitor who is not signed in attempts to access `GET /podcasts/new` or `POST /podcasts`.
2. The system redirects them to the magic-link sign-in page.

### User submits a valid podcast suggestion

1. A signed-in user fills in the required fields (title, feed URL, slug, main color hex, and an image file) and submits `POST /podcasts`.
2. The system validates all fields, including that any uploaded image is a real file with a filename no longer than 255 characters.
3. A new `Podcast` record is created with `published` set to `false` and `creator` set to the current user.
4. The system redirects the user to `/pod` and displays a success flash notice.

### User declares ownership at submission

1. A signed-in user checks the "I am the owner" checkbox before submitting.
2. After the podcast is saved successfully, the system assigns the `podcast_admin` role to the user for that podcast.

### Submission fails validation

1. A signed-in user submits the form with missing required fields, a duplicate feed URL or slug, an invalid `main_color_hex` format, or an image that is not a file or has a filename that is too long.
2. The system re-renders the suggestion form with a list of validation error messages.
3. No new podcast record is created.

## Failures / Exceptions

- If `main_color_hex` does not match the pattern `/\A([a-fA-F]|[0-9]){6}\Z/`, validation fails.
- If `feed_url` is not a valid HTTP or HTTPS URL, or is already used by another podcast, validation fails.
- If `slug` conflicts with an existing podcast, user username, organization slug, page slug, or reserved word, validation fails.
- If an uploaded image field receives a non-file value (e.g., a plain string), the controller short-circuits before saving and re-renders the form.
- If an uploaded image filename exceeds the allowed length, the controller similarly re-renders the form with an error.
