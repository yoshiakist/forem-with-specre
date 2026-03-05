---
id: "01KJ1NAP5PYW79V3ZJYHE3YZ69"
name: "author_can_embed_speakerdeck_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/speakerdeck_tag.rb`
- `app/views/liquids/_speakerdeck.html.erb` (Template)
- `spec/liquid_tags/speakerdeck_tag_spec.rb` (Test)

## Functional Overview

The `{% speakerdeck %}` Liquid tag allows authors to embed Speaker Deck presentations in articles. It accepts either a full `speakerdeck.com/player/` URL or a bare presentation ID (up to 32 alphanumeric characters). The tag extracts the ID and renders an iframe via the `_speakerdeck` partial. It is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches `speakerdeck.com/player/{id}` URLs (up to 32 chars)
- `VALID_ID_REGEXP` — matches bare alphanumeric IDs (up to 32 chars)
- `parse_input` — delegates to `pattern_match_for` with both patterns; extracts the `id` named group

## Scenarios

### Embedding a Speaker Deck by ID

1. Author writes `{% speakerdeck 7e9f8c0fa0c949bd8025457181913fd0 %}` in article body
2. System validates the ID matches `VALID_ID_REGEXP`
3. Rendered output is an iframe loading the Speaker Deck player

### Embedding a Speaker Deck by URL

1. Author pastes `https://speakerdeck.com/player/7e9f8c0fa0c949bd8025457181913fd0`
2. `UnifiedEmbed` matches `REGISTRY_REGEXP` and routes to `SpeakerdeckTag`
3. System extracts the ID and renders the embed iframe

## Failures / Exceptions

- IDs with spaces, special characters, or exceeding 32 characters raise `StandardError` with an i18n invalid-speakerdeck-id message
