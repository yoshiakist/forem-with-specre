---
id: "01KJ1FGS84AE316EVNASQ3GSCW"
name: "author_can_embed_vimeo_video_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/vimeo_tag.rb`
- `app/views/liquids/_vimeo.html.erb` (Template)
- `spec/liquid_tags/vimeo_tag_spec.rb` (Test)

## Functional Overview

An author can embed a Vimeo video into an article body by writing a `{% vimeo %}` Liquid tag with either a bare numeric video ID or any recognized Vimeo URL. The tag extracts the video ID, renders an iframe pointing to the Vimeo player at a fixed size of 710x399, and injects the result into the article HTML. The tag is also registered with `UnifiedEmbed` so that raw Vimeo URLs pasted into the editor are auto-converted to the same embed.

## Design Intent

Accepting multiple input forms (bare ID, canonical URL, player URL, markdown-linked URL) makes the tag forgiving for authors who copy a link from the browser address bar or from Vimeo's share dialog. Delegating rendering to a partial keeps the HTML template independently editable without touching Ruby logic. The fixed 710x399 dimensions match the standard content column width while maintaining a 16:9-ish aspect ratio.

## Key Members

- `REGISTRY_REGEXP` — regular expression that matches Vimeo video URLs in all supported forms and captures the numeric `video_id` group
- `@id` — the extracted Vimeo numeric video ID used as the iframe `src` path segment
- `@width` / `@height` — fixed embed dimensions (710 x 399); hardcoded, not author-configurable
- `PARTIAL` — path to the ERB partial (`liquids/vimeo`) that renders the iframe markup

## Scenarios

### Embed by bare video ID

1. Author writes `{% vimeo 205930710 %}` in an article body.
2. The tag strips surrounding whitespace from the token.
3. The token matches the `REGISTRY_REGEXP` and the numeric ID is captured; if it does not match, the token itself is used as the ID.
4. The tag renders the `_vimeo.html.erb` partial with `id`, `width`, and `height` locals.
5. The output is an `<iframe>` with `src="https://player.vimeo.com/video/205930710"`, `width="710"`, and `height="399"`.

### Embed by Vimeo canonical URL

1. Author writes `{% vimeo https://vimeo.com/205930710 %}` (or the bare `vimeo.com/205930710` form).
2. The tag strips HTML tags from the token and applies `REGISTRY_REGEXP`.
3. The video ID `205930710` is extracted from the URL path.
4. The same iframe as above is produced.

### Embed by Vimeo player URL

1. Author writes `{% vimeo https://player.vimeo.com/video/205930710 %}`.
2. `REGISTRY_REGEXP` matches the `player.vimeo.com/video/` path and extracts the ID.
3. The same iframe is produced.

### Embed from a markdown-linked URL

1. An editor or paste action converts a URL into `<a href="https://vimeo.com/205930710">https://vimeo.com/205930710</a>`.
2. The tag calls `strip_tags` on the token to remove HTML markup before matching.
3. The cleaned text is matched by `REGISTRY_REGEXP` and the video ID is extracted.
4. The same iframe is produced.

### Auto-embed via UnifiedEmbed

1. A raw Vimeo URL appears in article content that passes through `UnifiedEmbed`.
2. `UnifiedEmbed` matches the URL against `VimeoTag::REGISTRY_REGEXP` and delegates to `VimeoTag`.
3. The same iframe rendering path is followed.

## Failures / Exceptions

- Vimeo Showcase (album/collection) URLs are not supported; the ID extraction will fail or produce an unexpected result. This is a known limitation noted in the source.
- If the token contains no recognizable ID or URL segment, `get_id` returns the raw stripped token as the ID, which will produce a broken iframe src.
