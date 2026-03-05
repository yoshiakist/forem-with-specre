---
id: "01KJ1NAM3GKQ9Y3MWVQXGZBSH6"
name: "author_can_embed_neon_console_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/neon_tag.rb`
- `app/views/liquids/_neon.html.erb` (Template)

## Functional Overview

The `{% neon %}` Liquid tag is a stub implementation for embedding Neon database console content in articles. The `parse_id_or_url` method currently returns `true` unconditionally (no actual input validation or ID extraction). The tag renders via the `_neon` partial with whatever path value is set. It is **not** registered with `UnifiedEmbed` (no automatic URL detection), and there is no test file.

## Design Intent

This appears to be an incomplete or placeholder implementation. The `parse_id_or_url` method bypasses all validation, suggesting the feature was scaffolded but never finished. The `rubocop:disable Layout/LineLength` comment at the class level is vestigial.

## Key Members

- `parse_id_or_url` — always returns `true` (no validation)
- `@path` — set to the return value of `parse_id_or_url` (always `true`)

## Scenarios

### Embedding a Neon console (current behavior)

1. Author writes `{% neon <any input> %}` in article body
2. System accepts any input without validation
3. Partial renders with `path: true`

## Failures / Exceptions

- No validation errors are raised regardless of input (stub implementation)
