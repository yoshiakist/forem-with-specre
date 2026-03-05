---
id: "01KJ1N448SCYHT9ARSNBG5GPRH"
name: "author_can_embed_codesandbox_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/codesandbox_tag.rb`
- `app/views/liquids/_codesandbox.html.erb` (Template)
- `spec/liquid_tags/codesandbox_tag_spec.rb` (Test)

## Functional Overview

The `{% codesandbox %}` Liquid tag allows authors to embed CodeSandbox sandboxes in articles. The tag accepts either a bare sandbox ID (up to 60 alphanumeric characters) or a full codesandbox.io embed URL, with optional display parameters (`initialpath`, `file`, `module`, `view`, `runonclick`). The sandbox is rendered as a responsive iframe. The tag is also registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches codesandbox.io embed URLs, capturing the sandbox ID and optional query parameters
- `OPTIONS_REGEXP` — validates individual options: `initialpath`, `file`, `module`, `runonclick` (0 or 1), and `view` (editor, split, preview)
- `@id` — the extracted sandbox identifier
- `@query` — validated query string built from accepted options

## Scenarios

### Embedding with a bare sandbox ID

1. Author writes `{% codesandbox 22qaa1wcxr %}` in article body
2. System validates the ID matches the alphanumeric pattern (max 60 chars)
3. Rendered output is an iframe pointing to the CodeSandbox embed URL

### Embedding with ID and options

1. Author writes `{% codesandbox 43lkjfdauf initialpath=/path/file.js module=/path/to/module.html runonclick=1 view=split %}`
2. System validates each option against `OPTIONS_REGEXP`
3. Invalid options are silently filtered out; valid ones are joined into a query string
4. The iframe `src` includes the validated options

### Embedding via full URL

1. Author provides a full `https://codesandbox.io/embed/SANDBOX_ID?options` URL
2. System extracts the sandbox ID and options from the URL via `REGISTRY_REGEXP`
3. Options are re-validated through the same allowlist

## Failures / Exceptions

- Invalid sandbox ID (too long, special characters) raises `StandardError`
- All options go through allowlist validation; unrecognized options are silently dropped
