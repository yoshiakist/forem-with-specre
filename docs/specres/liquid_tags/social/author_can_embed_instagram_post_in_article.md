---
id: "01KJ1FKPG3YTDTTW2XT02SWA9T"
name: "author_can_embed_instagram_post_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/instagram_tag.rb`
- `app/views/liquids/_instagram.html.erb` (Template)
- `spec/liquid_tags/instagram_tag_spec.rb` (Test)

## Functional Overview

An article author can embed an Instagram post or profile by using the `{% instagram %}` Liquid tag in their article body. The tag accepts either a raw post ID (an 11-character alphanumeric string), a full Instagram post URL, or a profile URL. It resolves the input into the correct embed path and renders an iframe pointing to the Instagram embed endpoint, along with the Instagram embeds JavaScript loader.

## Design Intent

Instagram embeds are rendered as server-side iframes rather than client-side oEmbed calls to avoid third-party API rate limits and to produce consistent, fast markup at render time. The `InstagramTag` class inherits from `LiquidTagBase`, which provides shared pattern-matching and HTML-sanitization helpers used across all Liquid tags. Registering with `UnifiedEmbed` allows the tag to be triggered automatically when an Instagram URL is pasted as a bare link in article content.

## Key Members

- `REGISTRY_REGEXP` — matches full Instagram post URLs (`/p/<id>`) and profile URLs (`/<handle>`), used both for tag parsing and `UnifiedEmbed` auto-detection.
- `VALID_ID_REGEXP` — matches a bare 11-character post ID with no URL prefix.
- `@path` — the resolved embed path (e.g., `p/BXgGcAUjM39/embed/captioned/` for a post, or `somehandle/embed/` for a profile); passed as a local to the partial.
- `PARTIAL` (`"liquids/instagram"`) — the Rails partial that renders the iframe HTML.

## Scenarios

### Embed by post ID

1. Author writes `{% instagram BXgGcAUjM39 %}` in the article body.
2. `InstagramTag#initialize` receives the raw ID, strips HTML entities, and calls `parse_id_or_url`.
3. `parse_id_or_url` matches `VALID_ID_REGEXP` and returns the path `p/BXgGcAUjM39/embed/captioned/`.
4. `render` passes the path to the `_instagram` partial, which renders an `<iframe>` with `src="https://www.instagram.com/p/BXgGcAUjM39/embed/captioned/"` and loads the Instagram embeds script.

### Embed by post URL

1. Author writes `{% instagram https://www.instagram.com/p/BXgGcAUjM39/ %}` (or the tag is triggered automatically by `UnifiedEmbed` when a bare Instagram post URL is detected).
2. `parse_id_or_url` matches the URL against `REGISTRY_REGEXP`, extracts the `post_id` capture group, and returns `p/BXgGcAUjM39/embed/captioned/`.
3. The partial renders the same iframe as the post-ID scenario.

### Embed by profile URL

1. Author writes `{% instagram https://www.instagram.com/somehandle/ %}`.
2. `parse_id_or_url` matches `REGISTRY_REGEXP`, finds the `handle` capture group is present and non-empty, and returns `somehandle/embed/`.
3. The partial renders an iframe with `src="https://www.instagram.com/somehandle/embed/"`.

## Failures / Exceptions

- If the input does not match any of the accepted patterns (`REGISTRY_REGEXP` or `VALID_ID_REGEXP`), `parse_id_or_url` raises a `StandardError` with the localized message `liquid_tags.instagram_tag.invalid_instagram_id`, preventing the article from rendering the tag.
- Inputs longer than 30 characters for handle-style URLs, or post IDs that are not exactly 11 word characters/hyphens, are rejected as invalid.
