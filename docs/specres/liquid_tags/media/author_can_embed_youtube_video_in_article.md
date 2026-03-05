---
id: "01KJ1FH9QT2V3RGNJKW67RHNR5"
name: "author_can_embed_youtube_video_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/youtube_tag.rb`
- `app/views/liquids/_youtube.html.erb` (Template)
- `spec/liquid_tags/youtube_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a YouTube video into an article body by using the `{% youtube %}` or `{% embed %}` Liquid tag with a YouTube URL or bare video ID. The system extracts the 11-character video ID from short URLs (`youtu.be`), full watch URLs (`youtube.com/watch?v=`), or a bare ID, and renders a responsive iframe pointing to `https://www.youtube.com/embed/<id>`. When a start-time parameter (`t` or `start`) is present in the URL, the embedded player begins playback at that timestamp. The tag is also registered with `UnifiedEmbed`, so any YouTube URL pasted inline is automatically routed to this handler.

## Design Intent

Extracting the video ID and optional start time at parse time (in `initialize`) rather than at render time keeps the render step simple and side-effect-free. Raising `StandardError` immediately on an unrecognisable input gives authors fast, clear feedback before the article is saved. The fixed default dimensions (710 × 399) match a standard 16:9 aspect ratio suitable for most article widths.

## Key Members

- `@id` — The resolved embed token, either a bare 11-character video ID or `<id>?start=<seconds>` when a start time was detected.
- `@width` / `@height` — Fixed pixel dimensions passed to the iframe (710 × 399).
- `MARKER_TO_SECONDS_MAP` — Lookup table converting `h`, `m`, `s` suffix letters to their equivalent second counts, used when parsing human-readable time strings like `1h30m`.
- `YOUTUBE_REGEX` — Regular expression used by `UnifiedEmbed` to recognise YouTube URLs for automatic routing.

## Scenarios

### Embedding with a short URL (youtu.be)

1. Author writes `{% youtube https://youtu.be/vKeCr-MAyH4 %}` in the article body.
2. The tag strips any HTML entities and extracts the 11-character ID from the `youtu.be/` path segment.
3. The rendered output contains an iframe whose `src` is `https://www.youtube.com/embed/vKeCr-MAyH4`.

### Embedding with a full watch URL

1. Author writes `{% youtube https://www.youtube.com/watch?v=vKeCr-MAyH4 %}`.
2. The tag finds the `v=` query parameter and extracts the 11-character video ID.
3. The rendered iframe points to `https://www.youtube.com/embed/vKeCr-MAyH4`.

### Embedding with a bare video ID

1. Author writes `{% youtube vKeCr-MAyH4 %}` (exactly 11 alphanumeric/dash/underscore characters).
2. The tag accepts the string directly as the video ID without further URL parsing.
3. The rendered iframe points to `https://www.youtube.com/embed/vKeCr-MAyH4`.

### Embedding with a start-time parameter (numeric seconds)

1. Author uses a URL that includes `?t=231` or `?start=231`.
2. The tag extracts the numeric value and appends `?start=231` to the embed token.
3. The rendered iframe URL includes `?start=231`, causing the player to begin at that offset.

### Embedding with a human-readable start time (e.g., `1h30m`)

1. A URL contains a time parameter such as `t=1h30m`.
2. The tag parses each `h`/`m`/`s` component and converts them to a total second count (e.g., 5400).
3. The embed URL is constructed with `?start=5400`.

### Embedding via UnifiedEmbed (auto-routing)

1. Author pastes a raw YouTube URL (matching `youtu.be/`, `youtube.com/watch`, `youtube.com/embed`, `youtube.com/shorts`, or `youtube.com/live`) without an explicit tag.
2. `UnifiedEmbed` detects the URL, matches it against `YOUTUBE_REGEX`, and delegates to `YoutubeTag`.
3. The article renders the same iframe as if the author had written the tag explicitly.

## Failures / Exceptions

- If the input cannot be matched to any recognised URL pattern or bare ID format, `initialize` raises `StandardError` with the message "Invalid YouTube URL", preventing the article from rendering broken embed markup.
- Extraneous tracking parameters (e.g., `si=`) are silently ignored; only `v`, `t`, and `start` parameters affect the embed output.
