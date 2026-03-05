---
id: "01KJVGDRGWSEZX0907T1RXBTGD"
name: "system_transforms_html_for_article_display"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/html/parser.rb`
- `spec/services/html/parser_spec.rb` (Test)

## Functional Overview

`Html::Parser` is a chainable HTML transformation service used to prepare raw article HTML for display. It accepts an HTML string on initialization and exposes a set of instance methods — each returning `self` — that can be chained together to apply a sequence of DOM mutations using Nokogiri. Transformations include: stripping spurious `<br>` tags from list elements, routing images through Cloudinary or Giphy CDN, wrapping inline images in anchor tags, annotating code blocks with JavaScript-hook classes and a fullscreen control panel, wrapping tables in a scrollable container div, removing blank paragraphs, converting colon-syntax emoji aliases to Unicode outside of code elements, restoring obfuscated Liquid `{% raw %}`/`{% endraw %}` tags inside code blocks, grouping loose `<figcaption>` elements inside `<figure>` wrappers, turning `@username` mentions into profile links, and enforcing GIF-like attributes on `<video>` elements.

## Design Intent

The class uses the chainable builder pattern (each method returns `self`) so callers can compose exactly the transformations they need in a single expression without intermediate variables. Keeping every transformation as an independent method makes it easy to apply, test, and skip individual steps depending on context (e.g., email vs. web rendering).

## Key Members

- `html` (attr_accessor, read-only externally) — the mutable HTML string being transformed; read after the chain is complete to obtain the result.
- `RAW_TAG` / `END_RAW_TAG` — sentinel strings used to obfuscate Liquid `{% raw %}` tags during Markdown processing so they survive without side effects; `unescape_raw_tag_in_codeblocks` restores them.

## Scenarios

### Images are routed to CDN and wrapped in links

1. Caller invokes `prefix_all_images` on a parser instance containing `<img>` elements.
2. For each image whose host is not on the allow-list, the system rewrites the `src` through `Images::Optimizer` (Cloudinary) and marks the element `loading="lazy"`.
3. Giphy media URLs (`media.giphy.com`) are rewritten to `i.giphy.com` instead of Cloudinary.
4. If `synchronous_detail_detection: true` is passed, the system fetches actual pixel dimensions via `FastImage` and sets `width`/`height` attributes.
5. Caller then invokes `wrap_all_images_in_links`; each `<img>` inside a `<p>` that is not already inside an `<a>` is swapped for an anchor wrapping the image, using the image `src` as the href and `article-body-image-wrapper` as the CSS class.

### Code blocks receive interactive UI enhancements

1. Caller chains `add_control_class_to_codeblock`, which adds the `js-code-highlight` class to every `div.highlight` element, enabling JavaScript behavior.
2. Caller chains `add_control_panel_to_codeblock`, which appends a `div.highlight__panel.js-actions-panel` child to each `div.highlight`.
3. Caller chains `add_fullscreen_button_to_panel`, which inserts inline SVG icons for entering and exiting fullscreen mode into each `div.highlight__panel`.

### Emoji aliases outside code are converted to Unicode

1. Caller invokes `escape_colon_emojis_in_codeblock` on HTML that mixes plain text and `<code>` elements.
2. The system walks the DOM and converts `:alias:` patterns to Unicode emoji characters in every node that is not itself a `<code>` element and contains no `<code>` descendants.
3. Content inside `<code>` elements is left verbatim so that colon syntax is preserved for readers.

### Liquid raw tags obfuscated during rendering are restored in code blocks

1. The system encounters HTML where `{% raw %}` and `{% endraw %}` were encoded as `{----% raw %----}` and `{----% endraw %----}` during Markdown-to-HTML conversion to avoid Liquid processing.
2. Caller invokes `unescape_raw_tag_in_codeblocks`; the method performs a global string replace to restore the Liquid syntax.
3. Inside `<pre><code>` blocks, any residual `----` fragments that belong to the raw-tag encoding are also stripped, so the rendered code block shows clean `{% raw %}` / `{% endraw %}` text without extra dashes.
4. Four-dash sequences (`----`) that are unrelated to Liquid raw tags are left intact.

### Mentions, figures, and tables receive structural markup

1. Caller invokes `wrap_mentions_with_links`: text nodes containing `@username` patterns (outside `<code>` and `<a>` elements) are replaced with `<a class='mentioned-user'>` links if the username exists in the database.
2. Caller invokes `wrap_all_figures_with_tags`: any `<figcaption>` element not already inside a `<figure>` is grouped with its preceding sibling into a new `<figure>` wrapper; captions without a preceding sibling are left unchanged.
3. Caller invokes `wrap_all_tables`: each `<table>` element is swapped for a `<div class='table-wrapper-paragraph'>` containing the original table, enabling horizontal scrolling on narrow viewports.
4. Caller invokes `remove_nested_linebreak_in_list`: `<br>` elements nested directly inside `<ul>`, `<ol>`, or `<li>` elements are removed to prevent unwanted whitespace in rendered lists.
5. Caller invokes `remove_empty_paragraphs`: `<p>` elements whose only children are whitespace text nodes or `<br>` elements are deleted from the document.

## Failures / Exceptions

- All transformation methods tolerate `nil` or empty-string input gracefully — they return `self` without raising, producing no output or a no-op transformation.
- `parse_emojis` and `unescape_raw_tag_in_codeblocks` include explicit early-return guards (`return self if @html.blank?`) to avoid processing blank strings.
- When a `:alias:` colon sequence does not match any known emoji, `parse_emojis` leaves the original text unchanged rather than raising or substituting a placeholder.
- `wrap_mentions_with_links` performs a database lookup per unique mention; if no matching user is found, the raw `@username` text is preserved as-is.
