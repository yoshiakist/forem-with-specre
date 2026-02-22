---
id: "01KJ1FKR0TVDC2XEJ0TV56XPZY"
name: "author_can_embed_bluesky_post_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/bluesky_tag.rb`
- `app/views/liquids/_bluesky.html.erb` (Template)
- `spec/liquid_tags/bluesky_tag_spec.rb` (Test)

## Functional Overview

An article author can embed a Bluesky post into their article body by using the `{% bluesky %}` Liquid tag with either a standard Bluesky web URL or an AT-URI as the argument. The tag fetches the post's oEmbed HTML from Bluesky's embed endpoint and renders it inline via a partial template, producing a safe, embeddable iframe in the final article output.

## Design Intent

Bluesky uses the AT Protocol, so posts can be referenced by two formats: a human-facing web URL (`https://bsky.app/profile/.../post/...`) and a machine-facing AT-URI (`at://did:plc:.../app.bsky.feed.post/...`). Supporting both allows authors to paste whichever URL they have at hand. The tag normalizes both formats into a canonical web URL before calling the oEmbed endpoint, keeping the rendering path uniform. `valid_url?` is overridden to always return `true` so that `UnifiedEmbed` skips its own URL-fetching validation, avoiding a redundant HTTP round-trip.

## Key Members

- `REGISTRY_REGEXP` — matches a standard Bluesky web URL; used for `UnifiedEmbed` registration and URL parsing
- `VALID_ID_REGEXP` — matches an AT-URI (`at://did:plc:.../app.bsky.feed.post/...`); the alternate input format
- `@parsed` — hash containing `:url` (canonical web URL) and `:at_uri` produced by `parse_id_or_url`
- `@html` — raw HTML string returned by the oEmbed endpoint, rendered into the partial

## Scenarios

### Embed via web URL

1. Author writes `{% bluesky https://bsky.app/profile/did:plc:xxx/post/yyy %}` in the article body.
2. On render, the tag strips HTML entities from the input and matches it against `REGISTRY_REGEXP`.
3. The DID and post ID are extracted and stored as the canonical URL and AT-URI in `@parsed`.
4. The tag calls Bluesky's oEmbed endpoint (`https://embed.bsky.app/oembed?url=<canonical_url>`) with a `User-Agent` header identifying the community site.
5. The HTML string from the oEmbed response is passed to the `_bluesky` partial.
6. The partial renders the HTML as safe markup; the article page shows the embedded Bluesky post.

### Embed via AT-URI

1. Author writes `{% bluesky at://did:plc:xxx/app.bsky.feed.post/yyy %}` in the article body.
2. The tag matches the input against `VALID_ID_REGEXP` and extracts the DID and post ID.
3. A canonical web URL is constructed from those components; the original AT-URI is preserved as-is.
4. Rendering proceeds identically to the web URL scenario from step 4 onward.

### Invalid input is rejected

1. Author provides a string that matches neither `REGISTRY_REGEXP` nor `VALID_ID_REGEXP` (e.g., plain text or an unrelated URL).
2. `parse_id_or_url` raises `StandardError` with the message "Invalid Bluesky URL" during tag initialization.
3. The article fails to parse and the author receives an error indicating the tag input is invalid.

## Failures / Exceptions

- Any input not matching either accepted format raises `StandardError` ("Invalid Bluesky URL") at initialization time, before any HTTP call is made.
- If the oEmbed endpoint returns a non-200 response or a body without an `"html"` key, `@html` will be `nil` and the partial will render nothing (silent failure; no explicit error is raised).
