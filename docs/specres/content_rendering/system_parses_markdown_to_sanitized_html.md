---
id: "01KJ2XAF8C1H0K7QD5X08KHD2X"
name: "system_parses_markdown_to_sanitized_html"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/markdown_processor.rb`
- `app/services/markdown_processor/parser.rb`
- `app/sanitizers/rendered_markdown_scrubber.rb`
- `app/services/content_renderer.rb` (Tagged: 01KJ1C23JZY0T5QCNX103SR5MM)
- `app/services/giphy/image.rb`
- `app/services/html/image_uri.rb`
- `spec/services/content_renderer_spec.rb` (Test)
- `spec/services/markdown_processor/parser_spec.rb` (Test) (Tagged: 01KJ1C23JZY0T5QCNX103SR5MM)
- `spec/services/giphy/image_spec.rb` (Test)
- `spec/services/html/image_uri_spec.rb` (Test)

## Functional Overview

`MarkdownProcessor::Parser` converts a mixed Markdown and Liquid content string into final sanitized HTML through a multi-stage pipeline. It first guards against XSS patterns, normalizes legacy `<code>` block tags to triple-backtick fences, and wraps Liquid tags inside code spans with raw guards so they are not evaluated. It then renders the escaped content with Redcarpet (using `Redcarpet::Render::HTMLRouge` for syntax-highlighted code blocks) and immediately sanitizes the output with `RenderedMarkdownScrubber`, which enforces the `MarkdownProcessor::AllowedTags::RENDERED_MARKDOWN_SCRUBBER` and `MarkdownProcessor::AllowedAttributes::RENDERED_MARKDOWN_SCRUBBER` allowlists while preserving `class` attributes inside highlight code blocks. The sanitized result is then parsed as a Liquid template and re-rendered to expand any embedded Liquid tags, with the output passing through a final HTML post-processing chain (`Html::Parser`) that handles image prefixing, link wrapping, outbound link `target="_blank"` injection, mention linking, emoji escaping, and code block UI decoration. Context-specific rendering modes (`evaluate_markdown`, `evaluate_limited_markdown`, `evaluate_inline_limited_markdown`, `evaluate_listings_markdown`) use a simplified one-pass pipeline with tag allowlists appropriate for narrower display contexts such as sidebars, listings, or badges.

## Design Intent

The two-pass approach — render Markdown to HTML, sanitize, then parse and render Liquid — prevents Liquid tags embedded inside Markdown code blocks from being evaluated, because the `escape_liquid_tags_in_codeblock` step wraps them in `{% raw %}` guards before the Liquid pass. Code block `class` attributes are deliberately excluded from the attribute scrub step (handled separately in `RenderedMarkdownScrubber#scrub_attributes`) so that syntax-highlight class names added by Redcarpet are preserved through sanitization.

## Key Members

- `MarkdownProcessor::AllowedTags` — module grouping named tag allowlists per rendering context (e.g., `RENDERED_MARKDOWN_SCRUBBER`, `MARKDOWN_PROCESSOR_DEFAULT`, `MARKDOWN_PROCESSOR_LIMITED`, `MARKDOWN_PROCESSOR_INLINE_LIMITED`, `MARKDOWN_PROCESSOR_LISTINGS`)
- `MarkdownProcessor::AllowedAttributes` — parallel module grouping attribute allowlists per context
- `MarkdownProcessor::Parser#finalize` — full-pipeline renderer; accepts `link_attributes` and `prefix_images_options`
- `RenderedMarkdownScrubber` — extends `Rails::Html::PermitScrubber`; applies the `RENDERED_MARKDOWN_SCRUBBER` tag and attribute allowlists with special code-block handling

## Scenarios

### Full article render via finalize

1. Caller instantiates `MarkdownProcessor::Parser` with the raw content string, an optional source object, and a user.
2. `finalize` is called; the parser scans for XSS patterns (data-URI sources, HTML-entity-encoded ampersands) outside of code blocks and raises `ArgumentError` if any are found.
3. Bare `<code>` block tags are converted to triple-backtick fences, and Liquid tag syntax inside code spans and fenced blocks is wrapped with `{% raw %}` / `{% endraw %}` guards.
4. Redcarpet renders the preprocessed string to HTML with syntax highlighting via `Redcarpet::Render::HTMLRouge`.
5. The resulting HTML is passed through `RenderedMarkdownScrubber`, which strips disallowed tags and attributes and removes Liquid tag syntax from attribute values, while preserving `class` attributes inside syntax-highlight `div` and `span` elements.
6. The sanitized HTML is parsed as a Liquid template and rendered, expanding any embedded custom Liquid tags; Liquid syntax errors produce an error message string rather than raising to the caller.
7. External links (`href` starting with `http`) that do not match the app domain receive `target="_blank"` and `rel="noopener noreferrer"`.
8. The HTML passes through `Html::Parser` post-processing (image prefixing, wrapping images in links, gif-like video enforcement, code block UI controls, table wrapping, empty paragraph removal, emoji escaping, mention linking, figcaption wrapping) before being returned.

### Context-specific simplified render

1. Caller invokes one of the evaluate methods (`evaluate_markdown`, `evaluate_limited_markdown`, `evaluate_inline_limited_markdown`, `evaluate_listings_markdown`) with optional custom `allowed_tags`.
2. If content is blank, `nil` is returned immediately.
3. Redcarpet renders the content to HTML in a single pass without Liquid processing.
4. Rails sanitize strips tags not present in the context-specific allowlist and restricts attributes to `alt`, `href`, and `src`.

### Liquid tag discovery

1. Caller invokes `tags_used` to discover which Liquid tag classes appear in the content.
2. Liquid tags inside code blocks are escaped first so they are not counted.
3. The content is parsed as a Liquid template; each root node whose superclass is `LiquidTagBase` is collected.
4. A deduplicated array of tag classes is returned; a Liquid syntax error returns an empty array.

### XSS detection

1. During `finalize` or via direct call to `catch_xss_attempts`, code block content is stripped from the markdown string.
2. The remaining string is checked against `BAD_XSS_REGEX` patterns matching `src=` with data/entity values or inline `data:text/html` URIs.
3. If a match is found, `ArgumentError` is raised with a localized message; content safely inside code blocks is never flagged.

## Failures / Exceptions

- `ArgumentError` — raised by `catch_xss_attempts` when XSS patterns are detected outside of code blocks.
- `Liquid::SyntaxError` — caught during the Liquid render pass; the error message string is used as the rendered output instead of aborting.
- `NoMethodError` (containing `"line_number"`) — a known Liquid 5 compatibility issue; caught and logged, falling back to the pre-Liquid sanitized content.
