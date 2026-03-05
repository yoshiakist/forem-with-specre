---
id: "01KJ1N6Z63X89CXHE8KQDPB55N"
name: "author_can_embed_replit_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/replit_tag.rb`
- `app/views/liquids/_replit.html.erb` (Template)
- `spec/liquid_tags/replit_tag_spec.rb` (Test)

## Functional Overview

The `{% replit %}` Liquid tag allows authors to embed Replit projects in articles. The tag accepts either a bare address in `@user/project` format or a full replit.com URL. The address is extracted and used to construct the embed iframe. File anchors (e.g., `#file.js`) in URLs are accepted but stripped from the embed address. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Scenarios

### Embedding via bare address

1. Author writes `{% replit @user/my-project %}` in article body
2. System validates the address against the `@username/project-name` pattern
3. Rendered output is an iframe with the Replit embed URL

### Embedding via full URL

1. Author provides `https://replit.com/@user/my-project#file.js`
2. System extracts the `@user/my-project` address, stripping the file anchor
3. The iframe renders with the extracted address

## Failures / Exceptions

- Invalid address or non-replit.com URL raises `StandardError` with a localized message
- Usernames longer than 15 characters or project names longer than 60 characters are rejected
