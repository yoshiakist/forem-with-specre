---
id: "01KJ1FEDS2SAX1P5115F8ECN5T"
name: "author_can_embed_soundcloud_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/soundcloud_tag.rb`
- `app/views/liquids/_soundcloud.html.erb` (Template)
- `spec/liquid_tags/soundcloud_tag_spec.rb` (Test)

## Functional Overview

When an author writes `{% soundcloud <url> %}` in an article body, the system validates that the provided URL is a well-formed SoundCloud track or playlist URL, then renders an inline `<iframe>` that embeds the SoundCloud web player. The embed is read-only and auto-play is disabled by default, so visitors can choose to play the audio at their own discretion. Invalid or non-SoundCloud URLs are rejected at parse time with a descriptive error, preventing broken embeds from appearing in published articles.

## Design Intent

SoundCloud embeds are handled as a Liquid tag so they integrate into Forem's existing article rendering pipeline without requiring special-case logic in the editor or renderer. Parsing and validation happen at initialization time rather than at render time, which makes errors visible immediately during article saving rather than silently producing broken output. The tag is also registered with `UnifiedEmbed`, allowing the system to auto-embed SoundCloud URLs pasted as bare links.

## Key Members

- `REGISTRY_REGEXP` — matches any `http(s)://soundcloud.com` URL for `UnifiedEmbed` auto-detection
- `@link` — the sanitized and validated SoundCloud URL stored after initialization
- `valid_link?` — enforces that the URL follows the pattern `https://soundcloud.com/<username>/(sets/)?<slug>`, with username 3–25 characters and slug 3–255 characters, both restricted to alphanumerics, hyphens, and underscores
- `height` — fixed at 166 px when passed to the partial, matching the standard SoundCloud player height

## Scenarios

### Embedding a valid SoundCloud track

1. Author writes `{% soundcloud https://soundcloud.com/artist-name/track-title %}` in the article body.
2. The system strips any surrounding whitespace and HTML from the URL, then verifies it matches the expected SoundCloud URL pattern.
3. The validated URL is stored and, at render time, passed to the SoundCloud partial.
4. The partial produces an `<iframe>` pointing to `https://w.soundcloud.com/player/?url=<link>&auto_play=false` with a fixed height of 166 px, lazy loading enabled, and autoplay off.
5. The rendered iframe appears inline in the article body, allowing readers to play the track.

### Embedding a valid SoundCloud playlist (set)

1. Author writes `{% soundcloud https://soundcloud.com/artist-name/sets/playlist-title %}`.
2. The system recognises the `sets/` segment as a valid playlist path and passes validation.
3. The embed renders identically to a track embed, with the SoundCloud player loading the playlist.

### Auto-embedding a bare SoundCloud URL

1. Author pastes a bare `https://soundcloud.com/…` URL on its own line without a Liquid tag.
2. `UnifiedEmbed` matches the URL against `REGISTRY_REGEXP` and automatically delegates rendering to `SoundcloudTag`.
3. The article renders with the same iframe output as if the author had used the explicit tag.

## Failures / Exceptions

- If the URL does not match the expected `https://soundcloud.com/<username>/(sets/)?<slug>` pattern — including HTTP-only URLs, extra path segments, or missing username/slug — the system raises a `StandardError` with a localised message (`liquid_tags.soundcloud_tag.invalid_soundcloud_url`), and the article cannot be saved with that tag.
- Any embedded HTML or extraneous whitespace in the tag argument is stripped before validation, preventing injection via the tag syntax.
