---
id: "01KJ1NAMMQ8BXHGGFXQEYEW323"
name: "author_can_embed_next_tech_sandbox_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/next_tech_tag.rb`
- `app/views/liquids/_nexttech.html.erb` (Template)
- `spec/liquid_tags/next_tech_tag_spec.rb` (Test)

## Functional Overview

The `{% nexttech %}` Liquid tag allows authors to embed Next Tech coding sandboxes in articles. It accepts a `nt.dev/s/` share URL, extracts a 12-character lowercase alphanumeric token from the path, and renders an iframe pointing to `https://next.tech/projects/{token}/embed`. Query parameters and trailing slashes are stripped before validation. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches `https://nt.dev/s/` URLs
- `parse_share_url` — strips HTML tags and whitespace, removes query params, validates format, extracts trailing token
- `valid_share_url?` — requires exactly 12 lowercase alphanumeric characters after `nt.dev/s/`

## Scenarios

### Embedding a Next Tech sandbox

1. Author writes `{% nexttech https://nt.dev/s/6ba1fffbd09e %}` in article body
2. System strips query params and validates the 12-char token
3. Rendered output is an iframe at `https://next.tech/projects/6ba1fffbd09e/embed` with responsive height

### Automatic detection via UnifiedEmbed

1. Author pastes an `nt.dev/s/` URL into the editor
2. `UnifiedEmbed` matches `REGISTRY_REGEXP` and routes to `NextTechTag`

## Failures / Exceptions

- URLs not matching the `nt.dev/s/{12 alphanumeric chars}` pattern raise `StandardError` with an i18n invalid-url message
- Tokens with special characters or incorrect length are rejected
