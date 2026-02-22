---
id: "01KJ1NAFCEMR7CZQHG5PZPNMZF"
name: "author_can_embed_bandcamp_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/bandcamp_tag.rb`
- `app/views/liquids/_bandcamp.html.erb` (Template)
- `spec/liquid_tags/bandcamp_tag_spec.rb` (Test)

## Functional Overview

The `{% bandcamp %}` Liquid tag allows authors to embed Bandcamp albums and tracks in articles. Unlike most embed tags, this one fetches the Bandcamp page at render time to scrape embed IDs (`item_id`, `album_id`, `track_count`) from structured data attributes (`data-tralbum`, `bc-page-properties`, `og:video` meta tags). Album embeds have dynamic height based on track count (capped at 480px); track embeds use a fixed 120px height. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Design Intent

Bandcamp does not provide a public oEmbed or simple embed API. The tag must scrape the page HTML to extract the numeric IDs needed for the embedded player URL. Multiple fallback extraction strategies (data-tralbum JSON, bc-page-properties meta, og:video meta) ensure resilience against page structure changes.

## Key Members

- `BANDCAMP_URL_REGEX` — validates bandcamp.com album/track URLs
- `@embed_type` — `"album"` or `"track"`, extracted from URL path
- `fetch_bandcamp_ids_from_page_data` — HTTP-fetches the page and attempts three extraction strategies

## Scenarios

### Embedding a Bandcamp album

1. Author writes `{% bandcamp https://artist.bandcamp.com/album/my-album %}` in article body
2. System fetches the page and extracts the album ID and track count from structured data
3. Rendered output is an iframe with Bandcamp's EmbeddedPlayer showing the full tracklist
4. Height is calculated dynamically based on track count (128px + 40px per track, max 480px)

### Embedding a Bandcamp track

1. Author provides a track URL like `https://artist.bandcamp.com/track/my-song`
2. System extracts both the track ID and parent album ID from page data
3. Rendered output is a compact 120px iframe player for the single track

## Failures / Exceptions

- Invalid or non-bandcamp.com URL results in an inline error paragraph instead of raising
- If page scraping fails to extract sufficient IDs, a fallback paragraph with a direct Bandcamp link is rendered
- Network/HTTP errors are caught and logged; an inline "Error processing Bandcamp embed" message is returned
