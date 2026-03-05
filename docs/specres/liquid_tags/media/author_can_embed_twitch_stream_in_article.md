---
id: "01KJ1FGNZVJ8HD8PZ8VN9W22Y5"
name: "author_can_embed_twitch_stream_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/twitch_tag.rb`
- `app/views/liquids/_twitch.html.erb` (Template)
- `spec/liquid_tags/twitch_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a Twitch video or clip into an article body by using the `{% twitch %}` Liquid tag. The tag accepts either a bare video ID (numeric), a bare clip slug (alphanumeric with hyphens), or a full Twitch URL (player, clips, or embed variants). It resolves the input to the correct Twitch embed URL and renders a fixed-size iframe (710 x 399) pointing at the resolved URL, with autoplay disabled and the app domain set as the allowed parent.

## Design Intent

Twitch distinguishes between video embeds (`player.twitch.tv/?video=`) and clip embeds (`clips.twitch.tv/embed?clip=`). Because a clip slug matches the same character set as a video ID would if video IDs were not purely numeric, the tag checks against the numeric video-ID pattern first before falling back to the clip-slug pattern. This ordering prevents a numeric video ID from being misidentified as a clip slug. The `parent` parameter is derived from the app's configured domain (without port) to satisfy Twitch's same-origin embedding policy.

## Key Members

- `REGISTRY_REGEXP` — matches full Twitch URLs from `player.twitch.tv`, `clips.twitch.tv`, and `www.twitch.tv`; captures the raw ID or clip slug in the named group `id`
- `VALID_VIDEO_REGEXP` — matches a purely numeric string; captures in `video_id`
- `VALID_CLIP_REGEXP` — matches an alphanumeric-plus-hyphen string up to 100 characters; captures in `clip_slug`
- `@url` — resolved Twitch embed URL stored at initialization
- `@width` / `@height` — fixed iframe dimensions (710 x 399)

## Scenarios

### Embedding by bare video ID

1. Author writes `{% twitch 1196406756 %}` in the article body.
2. The tag strips any query-string parameters from the input to prevent parameter injection.
3. The input matches `VALID_VIDEO_REGEXP`, so the tag builds a `player.twitch.tv` URL with the video ID and `autoplay=false`.
4. The partial renders an iframe pointing at the player URL with the configured app domain as the parent.

### Embedding by bare clip slug

1. Author writes `{% twitch CuteSpicyNostrilDoritosChip %}` in the article body.
2. The tag strips any query-string parameters from the input.
3. The input does not match `VALID_VIDEO_REGEXP`; it matches `VALID_CLIP_REGEXP`, so the tag builds a `clips.twitch.tv/embed` URL with the clip slug and `autoplay=false`.
4. The partial renders an iframe pointing at the clip URL.

### Embedding by full Twitch URL

1. Author writes `{% twitch https://clips.twitch.tv/embed?clip=CuteSpicyNostrilDoritosChip %}` (or a player/www URL) in the article body.
2. The tag strips any query-string continuation after `&` to prevent parameter injection.
3. The input matches `REGISTRY_REGEXP`, capturing the raw identifier in the `id` group.
4. The tag re-checks the captured ID: if numeric it builds a player URL; if alphanumeric-with-hyphens it builds a clip URL.
5. The partial renders the corresponding iframe.

### UnifiedEmbed auto-detection

1. A Twitch URL appears in a context where `UnifiedEmbed` is active.
2. `UnifiedEmbed` matches the URL against `TwitchTag::REGISTRY_REGEXP` and delegates rendering to `TwitchTag`.
3. The tag resolves and renders the iframe as in the full-URL scenario above.

## Failures / Exceptions

- If the input does not match any of the three accepted patterns (bare video ID, bare clip slug, full Twitch URL), the tag raises a `StandardError` with the localized message `liquid_tags.twitch_tag.invalid_twitch_id`.
- Query-string parameters appended to a bare ID or slug (e.g., `{% twitch CuteSpicyNostrilDoritosChip&autoplay=true %}`) are silently stripped before validation, preventing parameter injection into the generated embed URL.
- Whitespace surrounding the input token is stripped before processing, so extra spaces and tabs do not cause a validation failure.
