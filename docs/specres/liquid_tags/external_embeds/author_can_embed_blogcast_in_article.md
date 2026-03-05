---
id: "01KJ1NAG2B0GM9BJT8H5W0JEHB"
name: "author_can_embed_blogcast_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/blogcast_tag.rb`
- `app/views/liquids/_blogcast.html.erb` (Template)
- `spec/liquid_tags/blogcast_tag_spec.rb` (Test)

## Functional Overview

The `{% blogcast %}` Liquid tag allows authors to embed Blogcast audio players in articles. It accepts either a bare numeric ID (up to 9 digits) or a full `blogcast.host/embed/` URL. The tag extracts the numeric `video_id` and renders an iframe via the `_blogcast` partial. It is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches `https://app.blogcast.host/embed/{id}` URLs
- `VALID_ID_REGEXP` — matches bare numeric IDs (1-9 digits)
- `parse_id_or_url` — delegates to `pattern_match_for` with both patterns; raises on mismatch

## Scenarios

### Embedding a Blogcast by numeric ID

1. Author writes `{% blogcast 1234 %}` in article body
2. System validates the ID matches `VALID_ID_REGEXP`
3. Rendered output is an iframe pointing to the Blogcast embed player

### Embedding a Blogcast by URL

1. Author pastes `https://app.blogcast.host/embed/5678` into the editor
2. `UnifiedEmbed` matches `REGISTRY_REGEXP` and routes to `BlogcastTag`
3. System extracts the numeric ID from the URL and renders the embed iframe

## Failures / Exceptions

- Non-numeric or oversized IDs raise `StandardError` with an i18n invalid-blogcast-id message
- URLs not matching either regexp pattern are rejected at parse time
