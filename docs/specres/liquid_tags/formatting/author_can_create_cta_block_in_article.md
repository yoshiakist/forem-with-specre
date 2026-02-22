---
id: "01KJ1F8YGQEQHN0WEB1JX4TP1N"
name: "author_can_create_cta_block_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/cta_tag.rb`
- `spec/liquid_tags/cta_tag_spec.rb` (Test)
- `app/views/liquids/_cta.html.erb` (Template)

## Functional Overview

An article author can embed a call-to-action (CTA) button in an article body by using the `{% cta %}` Liquid block tag. The tag accepts a URL as its argument and a text description as its block content. When rendered, it produces an anchor element styled as a branded button that links to the given URL with the given description text. The description is sanitized of all HTML tags and truncated to 128 characters to prevent layout issues and XSS.

## Design Intent

The tag is intentionally constrained to a single visual type (`branded`) at this stage, with the constant `TYPE_OPTIONS` structured to accommodate future type variants (e.g., `primary`, `secondary`) without breaking changes. Delegating rendering to a Rails partial (`liquids/_cta`) keeps display logic out of the tag class and allows the template to be updated independently of the Ruby logic.

## Key Members

- `@link` — The URL passed as the tag argument; HTML tags are stripped before storage.
- `DESCRIPTION_LENGTH` (128) — Maximum number of characters allowed in the rendered description. Truncation appends `...`.
- `TYPE_OPTIONS` — Array of permitted CTA visual types; currently only `branded`. First element is always used.
- `PARTIAL` (`"liquids/cta"`) — Rails partial path used for rendering the final HTML output.

## Scenarios

### Author embeds a CTA with a URL and description

1. Author writes `{% cta https://example.com %} Click here {% endcta %}` in an article body.
2. The system strips any HTML tags from the URL argument and stores it as the link target.
3. The system parses the block body, strips all HTML tags from it, and trims surrounding whitespace and newlines to produce the description text.
4. The system renders the `liquids/_cta` partial with the link, description, and `branded` type.
5. The rendered output is an `<a>` element with `class="ltag_cta ltag_cta--branded"`, `role="button"`, the correct `href`, and the description as its text content.

### Description exceeds 128 characters

1. Author provides a block body whose plain-text content is longer than 128 characters.
2. The system strips HTML tags, trims the text, and then truncates it to 128 characters, appending `...` at the cutoff point.
3. The rendered CTA displays the truncated description; any text beyond the limit is not shown.

### Description contains HTML markup

1. Author (or an attacker) includes HTML tags inside the CTA block body (e.g., `<div class='x'>DEV Community</div>`).
2. The system strips all HTML tags from the block content before using it as the description.
3. The rendered output contains only the plain text; no HTML attributes or tag syntax appear in the output.

## Failures / Exceptions

- If the URL argument itself contains HTML tags, they are stripped via `strip_tags` in `initialize`; the stored link is plain text only.
- An empty or whitespace-only description is permitted; the rendered anchor will have no visible text, but no error is raised.
