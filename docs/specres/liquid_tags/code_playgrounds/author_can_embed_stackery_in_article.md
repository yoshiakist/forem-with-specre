---
id: "01KJ1N70FN162EFMZ83MG5XGSN"
name: "author_can_embed_stackery_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/stackery_tag.rb`
- `app/views/liquids/_stackery.html.erb` (Template)
- `spec/liquid_tags/stackery_tag_spec.rb` (Test)

## Functional Overview

The `{% stackery %}` Liquid tag allows authors to embed Stackery infrastructure designer views in articles. The tag accepts either a full `app.stackery.io/editor/design` URL with query parameters or space-separated arguments (`owner repo [ref]`). Parameters (`owner`, `repo`, `file`, `ref`) are validated against an allowlist. The designer view is rendered as an iframe. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Scenarios

### Embedding via full URL

1. Author provides `https://app.stackery.io/editor/design?owner=my-org&repo=my-repo&ref=main`
2. System extracts and validates query parameters against `PARAM_REGEXP`
3. Rendered output is an iframe with the validated parameters

### Embedding via space-separated arguments

1. Author writes `{% stackery my-org my-repo main %}`
2. System builds the parameter string as `owner=my-org&repo=my-repo&ref=main`
3. If the third argument (ref) is omitted, it defaults to `master`

## Failures / Exceptions

- Missing owner or repo argument raises `StandardError` with a localized message
- Invalid URL format raises `StandardError`
