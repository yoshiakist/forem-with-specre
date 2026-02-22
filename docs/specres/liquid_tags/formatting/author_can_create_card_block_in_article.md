---
id: "01KJ1F6MWHBZ38XZ2ZHS73YNZA"
name: "author_can_create_card_block_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/card_tag.rb`
- `app/views/liquids/_card.html.erb` (Template)
- `spec/liquid_tags/card_tag_spec.rb` (Test)

## Functional Overview

An author can wrap arbitrary Markdown content in a `{% card %}...{% endcard %}` Liquid block tag within an article body. The system renders the inner content and wraps it in a styled card container, producing a visually distinct embedded card element in the published article.

## Design Intent

The tag is implemented as a `Liquid::Block` rather than a `Liquid::Tag` so that authors can place multi-line Markdown content between opening and closing delimiters instead of passing everything as a single inline argument. Delegating rendering to `ApplicationController.render` with a Rails partial keeps the HTML structure in a single ERB template, ensuring that styling changes can be made in one place without touching the tag class.

## Key Members

- `PARTIAL` — constant pointing to `liquids/card`, the ERB partial that wraps the rendered content in a card container
- `render(_context)` — calls `super` to obtain the inner block content (already processed by Liquid), then delegates to `ApplicationController.render` with the content passed as a local

## Scenarios

### Author embeds a card block with Markdown content

1. Author writes `{% card %} <markdown content> {% endcard %}` in an article body
2. The Liquid parser processes the block and calls `CardTag#render`
3. The inner Markdown content is retrieved via `super`
4. The system renders the `liquids/card` partial with the inner content as a local variable
5. The resulting HTML wraps the content in a `<div>` with the `crayons-card c-embed` CSS classes
6. The card HTML is embedded in the article's rendered output

### Rendered output contains the authored content

1. Author places Markdown text (e.g., a heading and inline code) inside the card block
2. The rendered card HTML includes the authored text
3. All authored text is present and readable within the card container

## Failures / Exceptions

- No explicit sanitization is applied inside the tag class itself; `html_safe` is called directly on `content` in the partial, so the safety of the content depends on upstream Liquid processing
