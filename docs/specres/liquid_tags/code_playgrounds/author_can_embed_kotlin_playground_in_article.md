---
id: "01KJ1N6YXN1WKW53P7WH7V5EZD"
name: "author_can_embed_kotlin_playground_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/kotlin_tag.rb`
- `app/views/liquids/_kotlin.html.erb` (Template)
- `spec/liquid_tags/kotlin_tag_spec.rb` (Test)

## Functional Overview

The `{% kotlin %}` Liquid tag allows authors to embed Kotlin Playground snippets in articles. The tag accepts a pl.kotl.in URL with optional query parameters (`theme=darcula`, `readOnly=true`, `from=N`, `to=N`). Parameters are validated against an allowlist; invalid ones are silently filtered. The playground is rendered as an iframe. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Scenarios

### Embedding a Kotlin playground

1. Author writes `{% kotlin https://pl.kotl.in/abc123 %}` in article body
2. System validates the URL matches the pl.kotl.in domain pattern
3. Rendered output is an iframe with the playground URL

### Embedding with display parameters

1. Author provides `https://pl.kotl.in/abc123?theme=darcula&readOnly=true`
2. System extracts parameters and validates each against `PARAM_REGEXP`
3. Valid parameters are preserved in the rebuilt URL; invalid ones are dropped

## Failures / Exceptions

- Invalid or non-pl.kotl.in URL raises `StandardError` with a localized message
