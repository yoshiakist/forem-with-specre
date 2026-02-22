---
id: "01KJ1NAKJ1F3VDFEZ8SCWFZ3D3"
name: "author_can_embed_medium_article_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/medium_tag.rb`
- `app/views/liquids/_medium.html.erb` (Template)
- `spec/liquid_tags/medium_tag_spec.rb` (Test)

## Functional Overview

The `{% medium %}` Liquid tag allows authors to embed Medium article previews in articles. It accepts a `medium.com` URL (including subdomain variants like `blog.medium.com` and `@user` profile paths), delegates to `MediumArticleRetrievalService` to scrape article metadata (title, author, author image, reading time, publication date), and renders a card with that metadata. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — matches `medium.com` URLs with optional subdomain and `@user` path segments
- `parse_url` — validates the URL via `pattern_match_for`, then calls `MediumArticleRetrievalService.new(url).call`
- `MediumArticleRetrievalService` — external service class that scrapes Medium page metadata

## Scenarios

### Embedding a Medium article

1. Author writes `{% medium https://medium.com/@user/my-article-abc123 %}` in article body
2. System validates the URL matches `REGISTRY_REGEXP`
3. `MediumArticleRetrievalService` fetches and parses the article metadata
4. Rendered card shows the article title, author name, author image, reading time, and publication date

## Failures / Exceptions

- Non-Medium URLs raise `StandardError` with "Invalid link URL or link URL does not exist"
- If `MediumArticleRetrievalService` raises any `StandardError` (network failure, parse failure), the same invalid-link error is re-raised
