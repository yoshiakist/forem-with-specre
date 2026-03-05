---
id: "01KJ1N6WWGNYT9JR9Y5EMDVG4K"
name: "author_can_embed_glitch_project_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/glitch_tag.rb`
- `app/views/liquids/_glitch.html.erb` (Template)
- `spec/liquid_tags/glitch_tag_spec.rb` (Test)

## Functional Overview

The `{% glitch %}` Liquid tag allows authors to embed Glitch projects in articles. The tag accepts a Glitch project slug, a full glitch.me/glitch.com URL, or a tilde-prefixed ID. It supports display options (`app`, `code`, `no-files`, `preview-first`, `no-attribution`, `file=`) that control the embedded editor's layout. The `path=` parameter from URL query strings is also supported and mapped to the `file=` option. Options are converted to Glitch embed query parameters. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches glitch.me and glitch.com URLs, capturing subdomain, slug, and query params
- `ID_REGEXP` — matches bare slug or tilde-prefixed ID
- `OPTIONS_TO_QUERY_PAIR` — maps human-readable options (`app`, `code`, `no-files`, etc.) to Glitch embed query parameters
- `@id` — the project slug
- `@query` — URL-encoded query string built from validated options

## Scenarios

### Embedding via project slug

1. Author writes `{% glitch my-project %}` in article body
2. System validates the slug and defaults to `file=index.html`
3. Rendered output is an iframe with Glitch embed URL and the default file path

### Embedding via full URL with path

1. Author provides `https://glitch.com/edit/#!/my-project?path=src/app.js`
2. System extracts slug from URL and maps `path=` parameter to the `file=` option
3. The embed opens to the specified file

### Embedding with display options

1. Author writes `{% glitch my-project app no-attribution %}`
2. `app` maps to `previewSize=100`, `no-attribution` maps to `attributionHidden=true`
3. If both `app` and `code` are specified, they cancel each other out

## Failures / Exceptions

- Invalid slug or URL raises `StandardError` with a localized message
- If all provided options are invalid, `StandardError` is raised
