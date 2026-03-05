---
id: "01KJ1F43YDG56WXEHMDW5X1X9A"
name: "author_can_embed_tag_badge_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/tag_tag.rb`
- `app/views/tags/_liquid.html.erb` (Template)
- `spec/liquid_tags/tag_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a styled tag badge inside an article body using the `{% tag <name> %}` Liquid tag. When the tag is rendered, the system looks up the tag by name (stripping any full URL prefix if provided), then produces an HTML badge showing the tag's name as a link, a follow button, and the tag's short summary. The badge border and box-shadow colors are derived from the tag's configured background and text colors, adjusted to a fixed brightness threshold to ensure legibility.

## Design Intent

The Liquid tag approach lets authors reference community tags inline without writing raw HTML. Accepting either a bare tag name or a full `/t/<name>` URL gives authors flexibility while keeping the implementation simple: the URL prefix is stripped before the database lookup. Color contrast is enforced programmatically via `Color::CompareHex` so the badge remains readable regardless of the tag's custom palette.

## Key Members

- `@tag` — the `Tag` ActiveRecord object resolved from the author's input
- `@follow_btn` — pre-rendered HTML for the follow button, built via `ApplicationHelper#follow_button`
- `@dark_color` — hex color string computed from the tag's `bg_color_hex` and `text_color_hex`, clamped to 88% brightness; used for the badge border and shadow
- `PARTIAL` — `"tags/liquid"`, the view partial that produces the final HTML

## Scenarios

### Author embeds a tag by name

1. Author writes `{% tag ruby %}` in an article body.
2. System strips whitespace from the input and looks up a `Tag` record whose `name` matches `ruby`.
3. System computes a border/shadow color from the tag's color attributes.
4. System renders the `tags/liquid` partial, producing a badge that contains the tag name as a link, a follow button, and the tag's short summary.
5. The rendered HTML is inserted into the article at the location of the Liquid tag.

### Author embeds a tag using a full URL

1. Author writes `{% tag https://forem.example.com/t/ruby %}` in an article body.
2. System strips the site URL prefix, reducing the input to `ruby`.
3. Lookup and rendering proceed identically to the bare-name scenario above.

### Tag badge displays color-adjusted styling

1. When the resolved tag has `bg_color_hex` and/or `text_color_hex` set, the system computes a color at 88% brightness from those values.
2. The resulting color is applied to the badge's `border-color` and `box-shadow` CSS properties.
3. If either color attribute is absent, the system falls back to `#000000` for the background and `#ffffff` for the text before computing brightness.

## Failures / Exceptions

- If the tag name does not match any existing `Tag` record, the system raises a `StandardError` with the localized message from `liquid_tags.tag_tag.invalid_tag_name`, preventing the article from rendering with a broken badge.
