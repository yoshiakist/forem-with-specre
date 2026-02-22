---
id: "01KJ1N448MTCNKVWNREJQA0P9Y"
name: "author_can_embed_codepen_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/codepen_tag.rb`
- `app/views/liquids/_codepen.html.erb` (Template)
- `spec/liquid_tags/codepen_tag_spec.rb` (Test)

## Functional Overview

The `{% codepen %}` Liquid tag allows authors to embed CodePen pens in articles. The tag accepts a codepen.io URL (supporting individual and team pens, `/pen/`, `/embed/`, and `/pen/preview/` paths) and optional display parameters (`default-tab`, `theme-id`, `height`, `editable`). The URL is converted to an embed path and rendered as a responsive iframe. The tag is also registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — validates codepen.io URLs with username (max 30 chars), pen/embed/preview paths, and alphanumeric pen IDs
- `@link` — the embed URL (pen paths are rewritten to embed paths)
- `@height` — iframe height in pixels (default 600, overridable via `height=` parameter)
- `@build_options` — validated query string for `default-tab`, `theme-id`, and `editable`

## Scenarios

### Embedding a CodePen pen via URL

1. Author writes `{% codepen https://codepen.io/user/pen/PENID %}` in article body
2. System validates the URL matches the codepen.io domain and path pattern
3. System rewrites `/pen/` to `/embed/` in the URL
4. Rendered output is an iframe pointing to the embed URL with default height of 600px and `default-tab=result`

### Embedding with display options

1. Author writes `{% codepen https://codepen.io/user/pen/PENID default-tab=js,result theme-id=40148 height=300 editable=true %}`
2. System validates each option against its allowed pattern
3. Invalid options are silently filtered out; valid ones are appended as query parameters
4. The `height` parameter sets the iframe height attribute and is included in the embed URL

### Embedding a team pen or preview pen

1. Author provides a URL with `/team/` path segment or `/pen/preview/` path
2. System accepts the URL and preserves the preview indicator in the embed path

## Failures / Exceptions

- Invalid or non-codepen.io URL raises `StandardError` with a localized message
- Username exceeding 30 characters is rejected
- XSS attempts (protocol-relative URLs, domain spoofing, injected attributes) are rejected by regex validation
- If all provided options are invalid (none pass validation), `StandardError` is raised with an invalid options message
