---
id: "01KJ1F9644RRQ7Y8YW7SBRR9HA"
name: "author_can_create_collapsible_details_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/details_tag.rb`
- `app/views/liquids/_details.html.erb`
- `spec/liquid_tags/details_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a native HTML collapsible section inside an article using the Liquid tags `{% details %}`, `{% collapsible %}`, or `{% spoiler %}`. The tag accepts a summary label as its argument and treats the block body as the collapsible content. When rendered, the content is sanitized to allow safe HTML elements (headings, lists, links, images, inline code, code blocks) while stripping dangerous tags and event-handler attributes. The output is a standard `<details>` / `<summary>` element pair that browsers expand and collapse natively.

## Design Intent

Three tag aliases (`details`, `collapsible`, `spoiler`) are registered so authors can choose the name that best matches their intent — spoiler warnings, collapsible answers, or generic detail blocks — without needing separate implementations. Sanitization is applied to the inner content through `RenderedMarkdownScrubber` so that arbitrary HTML passed from article Markdown cannot introduce XSS vectors. The summary text is also sanitized on `initialize` to guard against injection through the tag argument.

## Key Members

- `@summary` — the sanitized text shown as the clickable label of the `<summary>` element; taken from the tag argument and stripped of leading/trailing whitespace
- `PARTIAL` — the ERB template path (`"liquids/details"`) used to render the final `<details>` HTML fragment
- `RenderedMarkdownScrubber` — the scrubber applied to inner block content; determines which HTML tags and attributes are permitted

## Scenarios

### Author writes a collapsible block with plain text

1. Author writes `{% details Click to see the answer! %}` followed by plain-text content and `{% enddetails %}` in an article body.
2. The Liquid template engine parses the tag and calls `DetailsTag#initialize` with the summary string.
3. The block body is rendered by the parent `Liquid::Block` and then parsed by Nokogiri to extract the body inner HTML.
4. The extracted content is sanitized by `RenderedMarkdownScrubber`.
5. The sanitized summary and content are passed to the `liquids/details` partial, producing a `<details><summary>Click to see the answer!</summary>…</details>` fragment.

### Author uses the `collapsible` or `spoiler` alias

1. Author writes `{% collapsible … %}` or `{% spoiler … %}` in place of `{% details … %}`.
2. The Liquid template engine resolves the tag name to `DetailsTag` via the registered aliases.
3. Rendering proceeds identically to the `details` tag case and produces the same `<details>` HTML output.

### Author includes rich HTML content (headings, lists, links, images, code)

1. Author places HTML elements such as `<h2>`, `<ol>/<li>`, `<a>`, `<img>`, `<code>`, or a code-block structure (`<div class="highlight"><pre …><code>`) inside the block.
2. `RenderedMarkdownScrubber` evaluates each element and retains the permitted tags and attributes.
3. The rendered output includes those elements intact within the `<details>` wrapper.

### Content contains a `<div>` outside a code-block context

1. Author includes a bare `<div>` element in the block content.
2. `RenderedMarkdownScrubber` strips the `<div>` tag while preserving its text content.
3. The rendered output does not contain the word `div` but still includes the summary.

## Failures / Exceptions

- Tags deemed dangerous (`<script>`, `<object>`, and similar) are stripped entirely from the block content; their text content may or may not be preserved depending on the scrubber configuration, but the tag itself never appears in the output.
- Event-handler attributes such as `onclick` are removed from otherwise-permitted elements; other attributes on those elements (e.g., `alt`) are kept if permitted by the scrubber.
- The summary argument is sanitized at initialization time, so any HTML injected into the tag argument is neutralized before it reaches the template.
