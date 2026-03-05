---
id: "01KJ1NWEFRSNZ50SSZ3SA0A6FQ"
name: "author_can_embed_wikipedia_excerpt_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/wikipedia_tag.rb`
- `app/views/liquids/_wikipedia.html.erb` (Template)
- `spec/liquid_tags/wikipedia_tag_spec.rb` (Test)

## Functional Overview

The `{% wikipedia %}` Liquid tag allows authors to embed Wikipedia article excerpts in articles. It accepts any `*.wikipedia.org/wiki/` URL (supporting all language editions) and fetches content via Wikipedia's REST API. For plain article URLs, it uses the `/page/summary/` endpoint to get the article extract. For URLs with section anchors (`#Section`), it uses the `/page/mobile-sections/` endpoint to locate and extract the specific section content. The extracted HTML is cleaned up using Nokogiri to remove non-printable elements, hatnotes, references, figures, and superscripts; links are converted to plain text. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Design Intent

Wikipedia articles can be very long, so the tag provides focused excerpts rather than full content. The two API strategies — summary for whole articles, mobile-sections for anchored sections — ensure the most relevant content is extracted. The `text_clean_up` method strips Wikipedia-specific markup (reference numbers, disambiguation hatnotes, figure captions) that would be confusing in an embed context, and converts links to plain text since Wikipedia internal links would not function outside Wikipedia.

## Key Members

- `REGISTRY_REGEXP` — matches `https://{lang}.wikipedia.org/wiki/{title}` URLs
- `TEXT_CLEANUP_XPATH` — XPath expression targeting `div.noprint`, `div.hatnote`, `span.mw-ref`, `figure`, and `sup` elements
- `parse_page` — calls `/page/summary/{title}` for plain article URLs; returns title and `extract_html`
- `parse_page_with_anchor` — calls `/page/mobile-sections/{title}` for section URLs; searches `remaining.sections` for matching anchor
- `text_clean_up` — Nokogiri-based HTML sanitization removing non-essential elements and converting links to text
- `get_section_contents` — iterates response sections to find the one matching the anchor fragment

## Scenarios

### Embedding a Wikipedia article excerpt

1. Author writes `{% wikipedia https://en.wikipedia.org/wiki/Wikipedia %}` in article body
2. System calls `https://en.wikipedia.org/api/rest_v1/page/summary/Wikipedia`
3. Rendered card shows the article title and a clean HTML excerpt

### Embedding a specific section

1. Author writes `{% wikipedia https://en.wikipedia.org/wiki/Wikipedia#Diversity %}`
2. System calls `https://en.wikipedia.org/api/rest_v1/page/mobile-sections/Wikipedia`
3. System locates the section with `anchor == "Diversity"`
4. Rendered card shows "Wikipedia - Diversity" as title with the cleaned section content

### Multi-language support

1. Author provides `https://ja.wikipedia.org/wiki/...`
2. System extracts `"ja"` from the hostname and calls the Japanese Wikipedia API
3. Content is rendered in the appropriate language

## Failures / Exceptions

- Non-Wikipedia URLs or URLs with numeric-only language codes raise `StandardError` with invalid-wikipedia-url
- API 404 responses (non-existent articles) raise `StandardError` with article-not-found including API detail
- Section anchors not found in the article raise `StandardError` with section-not-found
