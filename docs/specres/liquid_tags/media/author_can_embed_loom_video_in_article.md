---
id: "01KJ1FCBM92477MPNYVC51VCS6"
name: "author_can_embed_loom_video_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/loom_tag.rb`
- `app/views/liquids/_loom.html.erb` (Template)
- `spec/liquid_tags/loom_tag_spec.rb` (Test)

## Functional Overview

When an author includes a Loom URL in the `{% embed %}` Liquid tag inside an article, the system extracts the video ID from the URL and renders a responsive iframe pointing to the Loom embed endpoint. The tag accepts share URLs, embed URLs, and `www`-prefixed variants, as well as URLs that contain query parameters. URLs whose path segments contain characters outside the alphanumeric set (e.g. underscores or dashes) are rejected with a validation error.

## Design Intent

Loom URLs that include query parameters fail the generic valid-URL check used elsewhere in the liquid tag infrastructure, so query parameters are stripped before validation rather than rejected outright. Regardless of whether the author supplies a `share` or `embed` URL, the rendered output always uses the `embed` path to ensure the correct player interface is shown. The tag is registered with `UnifiedEmbed` so that bare Loom URLs pasted into articles are automatically routed to this tag without requiring the explicit `{% loom %}` syntax.

## Key Members

- `REGISTRY_REGEXP` — Regular expression that matches both `loom.com` and `www.loom.com` URLs using either the `share` or `embed` path segment, capturing the video ID as a named group `video_id`. An optional query-string suffix is allowed.
- `@id` — The extracted alphanumeric video ID, passed to the partial as a local variable for rendering.
- `PARTIAL` — The path `"liquids/loom"` referencing the ERB template that produces the iframe markup.

## Scenarios

### Embedding a share URL

1. Author writes `{% embed https://loom.com/share/<video_id> %}` in an article.
2. The system strips any HTML tags and unescapes HTML entities from the input.
3. The video ID is extracted from the URL via the registry pattern.
4. The system renders the `_loom.html.erb` partial with the extracted ID.
5. The article displays a responsive iframe with `src` set to `https://loom.com/embed/<video_id>`.

### Embedding an embed URL directly

1. Author provides a `loom.com/embed/<video_id>` URL instead of a share URL.
2. The system matches the URL with the same registry pattern and extracts the video ID.
3. The rendered iframe uses `https://loom.com/embed/<video_id>` as the source.

### Embedding a www-prefixed URL

1. Author provides a `www.loom.com/share/<video_id>` URL.
2. The system recognises the optional `www.` prefix and extracts the video ID.
3. The rendered iframe uses the canonical `loom.com/embed/<video_id>` source.

### Embedding a URL with query parameters

1. Author provides a Loom share URL that includes a query string (e.g. `?sharedAppSource=personal_library`).
2. The system removes the query string before applying the pattern match.
3. The video ID is extracted successfully and the iframe is rendered without the query string.

## Failures / Exceptions

- If the URL contains path characters outside the alphanumeric set (such as underscores or dashes in the video ID segment), the pattern match fails and the system raises a `StandardError` with the localised message from `liquid_tags.loom_tag.invalid_loom_url`.
- Any URL that does not match the `loom.com/share` or `loom.com/embed` structure also triggers the same validation error.
