---
id: "01KJ1N6ZQEV4F550YYB4QEJFDF"
name: "author_can_embed_stackblitz_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/stackblitz_tag.rb`
- `app/views/liquids/_stackblitz.html.erb` (Template)
- `spec/liquid_tags/stackblitz_tag_spec.rb` (Test)

## Functional Overview

The `{% stackblitz %}` Liquid tag allows authors to embed StackBlitz projects in articles. The tag accepts a bare project ID, a `stackblitz.com/edit/` URL, or a legacy `*.stackblitz.io` subdomain URL. It supports numerous display parameters (`view`, `file`, `embed`, `hideExplorer`, `hideNavigation`, `theme`, `ctl`, `devtoolsheight`, `hidedevtools`, `initialpath`, `showSidebar`, `terminalHeight`, `startScript`). Parameters can come from URL query strings or space-separated arguments. The embed is rendered as an iframe at a fixed height of 500px. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches `stackblitz.com/edit/ID` and `ID.stackblitz.io` URLs with optional query params
- `ID_REGEXP` — matches bare project IDs (alphanumeric + hyphens, max 60 chars)
- `PARAM_REGEXP` — validates individual display parameters against the allowlist

## Scenarios

### Embedding via bare ID

1. Author writes `{% stackblitz my-project %}` in article body
2. System validates the ID and renders an iframe at 500px height with no additional params

### Embedding via URL with parameters

1. Author provides `https://stackblitz.com/edit/my-project?file=src/app.js&theme=dark`
2. System extracts the ID and query parameters from the URL
3. Each parameter is validated against `PARAM_REGEXP`; invalid ones are dropped

### Embedding with space-separated options

1. Author writes `{% stackblitz my-project view=preview hideNavigation=1 %}`
2. System splits the input and validates each option
3. Valid options are joined into the embed query string

## Failures / Exceptions

- Invalid project ID raises `StandardError` with a localized message
- Unrecognized parameters are silently filtered out
