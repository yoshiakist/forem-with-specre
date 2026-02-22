---
id: "01KJ1N6YC7D22BXFDC9RKFZTF8"
name: "author_can_embed_jsitor_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/jsitor_tag.rb`
- `app/views/liquids/_jsitor.html.erb` (Template)
- `spec/liquid_tags/jsitor_tag_spec.rb` (Test)

## Functional Overview

The `{% jsitor %}` Liquid tag allows authors to embed Jsitor code playgrounds in articles. The tag accepts either a bare snippet ID or a full jsitor.com embed URL. Bare IDs are automatically prefixed with the jsitor.com embed URL. The playground is rendered as an iframe at a fixed height of 400px. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Scenarios

### Embedding via bare ID

1. Author writes `{% jsitor abc123 %}` in article body
2. System validates the ID against the alphanumeric pattern
3. System constructs the embed URL `https://jsitor.com/embed/abc123`
4. Rendered output is an iframe at 400px height

### Embedding via full URL

1. Author provides `https://jsitor.com/embed/abc123`
2. System validates against `REGISTRY_REGEXP` and uses the URL as-is

## Failures / Exceptions

- Invalid ID or non-jsitor.com URL raises `StandardError` with a localized message
- HTML entities in input are unescaped and `amp;` artifacts are stripped before validation
