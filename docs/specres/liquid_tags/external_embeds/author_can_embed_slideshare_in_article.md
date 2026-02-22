---
id: "01KJ1NANNC8GEF0RZHC90FS5EJ"
name: "author_can_embed_slideshare_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/slideshare_tag.rb`
- `app/views/liquids/_slideshare.html.erb` (Template)
- `spec/liquid_tags/slideshare_tag_spec.rb` (Test)

## Functional Overview

The `{% slideshare %}` Liquid tag allows authors to embed SlideShare presentations in articles. It accepts either a full `slideshare.net/slideshow/embed_code/key/` URL or a bare embed key (12-14 alphanumeric characters). The rendered iframe has a fixed height of 487px. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches `slideshare.net/slideshow/embed_code/key/{id}` URLs
- `VALID_ID_REGEXP` — matches bare 12-14 character alphanumeric keys
- `parse_input` — delegates to `pattern_match_for` with both patterns; extracts the `id` named group

## Scenarios

### Embedding a SlideShare by embed key

1. Author writes `{% slideshare rdOzN9kr1yK5eE %}` in article body
2. System validates the key matches `VALID_ID_REGEXP` (12-14 alphanumeric chars)
3. Rendered output is an iframe at 487px height with the SlideShare embed

### Embedding a SlideShare by URL

1. Author pastes `https://www.slideshare.net/slideshow/embed_code/key/NM9EY9oYslwfE`
2. `UnifiedEmbed` matches `REGISTRY_REGEXP` and routes to `SlideshareTag`
3. System extracts the key and renders the same 487px iframe

## Failures / Exceptions

- Keys not matching either pattern (wrong length or non-alphanumeric characters) raise `StandardError` with an i18n invalid-slideshare-key message
