---
id: "01KJ1FEC2H01BD97D0SV7SF10B"
name: "author_can_embed_mux_video_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/mux_tag.rb`
- `app/views/liquids/_mux.html.erb` (Template)
- `spec/liquid_tags/mux_tag_spec.rb` (Test)

## Functional Overview

When an author includes a Mux player URL in the `{% embed %}` Liquid tag inside an article, the system extracts the video ID from the URL and renders a responsive iframe pointing to the Mux player endpoint. The tag accepts URLs of the form `https://player.mux.com/<video_id>` with an optional query string, and renders the video at a fixed default size of 710×399. URLs that do not match the expected Mux player pattern are rejected with a validation error.

## Design Intent

Mux URLs may carry query parameters (e.g. `?autoplay=true`) that would cause the generic URL validation in the liquid tag infrastructure to fail. The implementation strips query parameters before applying the pattern match so that such URLs are accepted rather than rejected. The tag is registered with `UnifiedEmbed` using `skip_validation: true`, which allows bare Mux player URLs pasted into articles to be automatically routed to this tag without requiring the explicit `{% mux %}` syntax and without re-running the standard URL validation.

## Key Members

- `REGISTRY_REGEXP` — Regular expression that matches `https://player.mux.com/<video_id>` URLs, capturing the video ID as a named group `video_id`. An optional query-string suffix is allowed.
- `@id` — The extracted video ID (alphanumeric characters, dashes, and underscores), passed to the partial as a local variable for rendering.
- `@width` / `@height` — Fixed default dimensions of 710 and 399, used both as explicit `width`/`height` attributes and to compute the iframe's CSS `aspect-ratio`.
- `PARTIAL` — The path `"liquids/mux"` referencing the ERB template that produces the iframe markup.

## Scenarios

### Embedding a Mux player URL

1. Author writes `{% embed https://player.mux.com/<video_id> %}` in an article.
2. The system strips any HTML tags and unescapes HTML entities from the input.
3. The video ID is extracted from the URL via the registry pattern.
4. The system renders the `_mux.html.erb` partial with the extracted ID and default dimensions.
5. The article displays an iframe with `src` set to `https://player.mux.com/<video_id>`, `width="710"`, `height="399"`, `allowfullscreen`, and `loading="lazy"`.

### Embedding a URL with query parameters

1. Author provides a Mux player URL that includes a query string (e.g. `?autoplay=true`).
2. The system removes the query string before applying the pattern match.
3. The video ID is extracted successfully and the iframe is rendered without the query string.

### Automatic routing via UnifiedEmbed

1. Author pastes a bare `https://player.mux.com/<video_id>` URL into an article without using the explicit `{% embed %}` syntax.
2. `UnifiedEmbed` matches the URL against `REGISTRY_REGEXP` and routes it to `MuxTag`.
3. The system renders the same iframe output as if the explicit tag had been used.

## Failures / Exceptions

- If the input URL does not match the `https://player.mux.com/<video_id>` structure, the pattern match fails and the system raises a `StandardError` with the localised message from `liquid_tags.mux_tag.invalid_mux_url`.
- Any URL pointing to a domain other than `player.mux.com`, or with a path that contains characters outside the allowed set (`[a-zA-Z0-9_-]`), also triggers the same validation error.
