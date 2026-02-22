---
id: "01KJ1FEG9MH1RKHEPHQ2449TTQ"
name: "author_can_embed_spotify_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/spotify_tag.rb`
- `app/views/liquids/_spotify.html.erb` (Template)
- `spec/liquid_tags/spotify_tag_spec.rb` (Test)

## Functional Overview

An author can embed a Spotify player inside an article body by using the `{% spotify %}` Liquid tag. The tag accepts a Spotify URI (e.g. `spotify:track:<id>`) or a Spotify open.spotify.com registry URL. It parses the content type and item identifier from the input, selects an appropriate player height based on the content type, and renders an embedded iframe pointing to `https://open.spotify.com/embed/<type>/<id>`. The tag is also registered with `UnifiedEmbed` so that bare Spotify URLs pasted into articles are auto-embedded.

## Design Intent

Spotify content types (track, album, artist, playlist, episode, show) have different natural display heights. Rather than using a single fixed height, the tag maps each type to a recommended pixel height so that the embedded player looks correct without requiring authors to specify dimensions explicitly. Legacy user-scoped playlist URIs (`spotify:user:<user>:playlist:<id>`) are supported to avoid breaking existing articles.

## Key Members

- `REGISTRY_REGEXP` — matches open.spotify.com URLs; used for both input parsing and `UnifiedEmbed` auto-detection
- `URI_REGEXP` — matches the standard Spotify URI format `spotify:<type>:<id>`
- `URI_PLAYLIST_REGEXP` — matches the legacy user-scoped playlist URI format for backwards compatibility
- `TYPE_HEIGHT` — maps each Spotify content type to its iframe pixel height (track: 80, episode/show: 232, others: 380)
- `@type` — the parsed Spotify content type (e.g. `"track"`, `"playlist"`)
- `@id` — the parsed Spotify item identifier (alphanumeric, up to 22 characters)
- `@height` — the iframe height in pixels derived from `TYPE_HEIGHT` based on `@type`

## Scenarios

### Embed a track via Spotify URI

1. Author writes `{% spotify spotify:track:0K1UpnetfCKtcNu37rJmCg %}` in the article body.
2. The tag parses the URI, extracting type `track` and id `0K1UpnetfCKtcNu37rJmCg`.
3. Height is set to 80px (the value for tracks).
4. The tag renders a lazy-loading iframe pointing to `https://open.spotify.com/embed/track/0K1UpnetfCKtcNu37rJmCg` at 100% width and 80px height.

### Embed a playlist via Spotify URI

1. Author writes `{% spotify spotify:playlist:37i9dQZF1E36t2Deh8frhL %}` in the article body.
2. The tag parses the URI, extracting type `playlist` and the playlist id.
3. Height is set to 380px (the value for playlists).
4. An iframe for the playlist embed is rendered at 380px height.

### Embed content via an open.spotify.com URL

1. Author pastes an `https://open.spotify.com/<type>/<id>` URL (optionally with a `?si=` query parameter) into the article.
2. The tag or `UnifiedEmbed` matches the URL against `REGISTRY_REGEXP`.
3. Type and id are extracted, height is determined, and the iframe is rendered.

### Embed a legacy user-scoped playlist URI

1. Author writes a URI in the form `spotify:user:<user>:playlist:<id>`.
2. The tag matches it against `URI_PLAYLIST_REGEXP` and extracts the playlist id; type defaults to the user field value captured by the regex.
3. The iframe is rendered without raising an error, preserving backward compatibility.

## Failures / Exceptions

- If the input does not match any of the three supported patterns (`REGISTRY_REGEXP`, `URI_REGEXP`, `URI_PLAYLIST_REGEXP`), the tag raises a `StandardError` with the message from `liquid_tags.spotify_tag.invalid_spotify_uri` (rendered to the user as "Invalid Spotify URI or URL.").
