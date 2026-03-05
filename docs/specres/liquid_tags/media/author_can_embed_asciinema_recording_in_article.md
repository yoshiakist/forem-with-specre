---
id: "01KJ1FC5TTWJKZS6HXP58WKM8Y"
name: "author_can_embed_asciinema_recording_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/asciinema_tag.rb`
- `app/views/liquids/_asciinema.html.erb` (Template)
- `spec/liquid_tags/asciinema_tag_spec.rb` (Test)

## Functional Overview

An author can embed an Asciinema terminal recording in an article body by using the `{% asciinema <id> %}` Liquid tag. The tag accepts either a bare recording ID (numeric or alphanumeric base64url) or a full asciinema.org URL. It extracts the recording ID, validates its format, and renders an inline `<script>` embed that loads the player asynchronously from asciinema.org.

## Design Intent

The tag accepts both bare IDs and full asciinema.org URLs so that authors can paste either form directly from their browser. The ID is extracted from the URL with a regex rather than a generic URL parser to prevent accepting IDs hosted on other domains. Validation rejects characters outside the numeric and base64url alphabets (letters, digits, `_`, `-`) before any HTML is rendered, stopping injection at parse time. The tag is also registered with `UnifiedEmbed` so that a bare URL in article body text can be auto-converted to this tag without requiring the author to write the Liquid tag syntax manually.

## Key Members

- `REGISTRY_REGEXP` — matches a full `https://asciinema.org/a/<id>` URL and captures the recording ID; also used by `UnifiedEmbed` to detect embeddable URLs
- `@id` — the extracted and validated recording ID, passed to the partial as a local variable
- `PARTIAL` — path to the ERB partial (`liquids/asciinema`) that renders the embed `<script>` tag

## Scenarios

### Embedding with a bare numeric ID

1. Author writes `{% asciinema 1234 %}` in the article body.
2. The tag strips surrounding whitespace from the input and finds no URL match.
3. The ID `1234` passes the numeric validation rule.
4. The partial renders a `<div class="ltag_asciinema">` containing a `<script>` tag that asynchronously loads the Asciinema player from `https://asciinema.org/a/1234.js`.

### Embedding with a bare alphanumeric base64url ID

1. Author writes `{% asciinema abc123_-XYZ %}` in the article body.
2. The tag strips surrounding whitespace and finds no URL match.
3. The ID `abc123_-XYZ` passes the base64url validation rule (letters, digits, `_`, `-`).
4. The partial renders the Asciinema player embed for that ID.

### Embedding with a full asciinema.org URL

1. Author writes `{% asciinema https://asciinema.org/a/1234 %}` (or pastes the URL as a bare link that `UnifiedEmbed` converts).
2. The tag matches the URL against `REGISTRY_REGEXP` and extracts the ID `1234`.
3. No additional validation is needed; the captured ID is used directly.
4. The partial renders the embed for the extracted ID.

## Failures / Exceptions

- An ID containing characters outside `[A-Za-z0-9_-]` (e.g. `inv@lid`, `abc+123`, `abc=123`, `abc/123`) causes the tag to raise an error with the localised message `liquid_tags.asciinema_tag.invalid_asciinema_id` at parse time; the article cannot be saved with this tag.
- A URL that does not match the `https://asciinema.org/a/<id>` pattern (e.g. `https://example.com/a/1234`) is not recognised as a URL and falls through to bare-ID validation, where it fails because it contains characters like `:`, `/`, and `.`; an error is raised.
