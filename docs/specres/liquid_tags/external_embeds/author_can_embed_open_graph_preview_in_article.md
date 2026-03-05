---
id: "01KJ1NAN64NZQV4VXD5BHDSD1T"
name: "author_can_embed_open_graph_preview_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/open_graph_tag.rb`
- `app/views/liquids/_open_graph.html.erb` (Template)

## Functional Overview

The `OpenGraphTag` is a fallback Liquid tag that renders a rich link preview for any URL by fetching its Open Graph metadata. Unlike other embed tags, it is **not** registered in the `UnifiedEmbed` registry and has no dedicated `{% opengraph %}` syntax — it is invoked programmatically when no other handler matches a URL. It uses the `OpenGraph` gem to fetch the page and extract `og:title`, `og:description`, `og:image`, and similar meta tags. The domain (minus `www.`) is extracted from the URL for display.

## Design Intent

This tag serves as the universal fallback for URLs that no specialized embed tag can handle. By fetching Open Graph metadata, it provides a minimal but informative preview card rather than a raw link.

## Key Members

- `@page` — `OpenGraph.new(url)` instance containing parsed OG metadata
- `@url_domain` — host extracted from the URL with `www.` prefix stripped
- No `REGISTRY_REGEXP` — intentionally not registered for automatic detection

## Scenarios

### Rendering an Open Graph preview for an unrecognized URL

1. A URL is encountered that no registered embed handler matches
2. System creates an `OpenGraphTag` with the URL
3. `OpenGraph.new(url)` fetches the page and parses OG meta tags
4. Rendered card shows the page title, description, image, and domain

## Failures / Exceptions

- If the URL is malformed, `URI.parse` raises (not caught by the tag)
- Network failures in `OpenGraph.new` propagate as-is
- No test file exists for this tag
