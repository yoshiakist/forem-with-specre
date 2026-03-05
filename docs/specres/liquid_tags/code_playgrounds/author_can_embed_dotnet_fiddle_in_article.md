---
id: "01KJ1N448WPGKRDWX23FHQM5FT"
name: "author_can_embed_dotnet_fiddle_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/dotnet_fiddle_tag.rb`
- `app/views/liquids/_dotnetfiddle.html.erb` (Template)
- `spec/liquid_tags/dotnet_fiddle_tag_spec.rb` (Test)

## Functional Overview

The `{% dotnetfiddle %}` Liquid tag allows authors to embed .NET Fiddle code snippets in articles. The tag accepts a dotnetfiddle.net URL (with or without the `/Widget/` path segment) and renders an iframe at a fixed height of 600px. If the URL does not already include `/Widget/`, the system automatically rewrites it to the widget embed path. The tag is also registered with `UnifiedEmbed` for automatic URL detection.

## Scenarios

### Embedding a .NET Fiddle snippet

1. Author writes `{% dotnetfiddle https://dotnetfiddle.net/Widget/v2kx9jcd %}` in article body
2. System validates the URL matches the dotnetfiddle.net domain pattern
3. Rendered output is an iframe with the widget URL and height of 600px

### Auto-rewriting to widget path

1. Author provides a URL without `/Widget/` (e.g., `https://dotnetfiddle.net/v2kx9jcd`)
2. System detects the missing widget path and rewrites to `https://dotnetfiddle.net/Widget/v2kx9jcd`
3. The iframe renders with the rewritten URL

## Failures / Exceptions

- Invalid or non-dotnetfiddle.net URL raises `StandardError` with a localized message
- XSS attempts (protocol-relative URLs, domain spoofing) are rejected by regex validation
