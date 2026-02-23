---
id: "01KJ2XAS3VHER16YT45BKAW3YF"
name: "system_converts_html_to_markdown"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/lib/reverse_markdown/converters/custom_pre.rb`
- `app/lib/reverse_markdown/converters/custom_text.rb`
- `spec/lib/reverse_markdown/converters/custom_pre_spec.rb` (Test)
- `spec/lib/reverse_markdown/converters/custom_text_spec.rb` (Test)

## Functional Overview

The system provides two custom ReverseMarkdown converters that transform specific HTML elements into Markdown. `CustomPre` converts `<pre>` blocks into either GitHub-flavored fenced code blocks (triple backticks with an optional language identifier) or 4-space-indented code blocks, depending on the `github_flavored` configuration flag. It detects the programming language from three CSS class naming conventions: `language-<lang>` on the `<pre>` element itself, `highlight-<lang>` on the parent element, and Confluence-style `brush:<lang>;`. `CustomText` converts HTML text nodes into clean Markdown text by stripping leading and trailing newlines, collapsing internal whitespace, converting non-breaking spaces to the `&nbsp;` HTML entity, escaping Markdown special characters, and then restoring those characters inside backtick-enclosed inline code spans.

## Design Intent

The two converters extend the `Base` class of the `ReverseMarkdown` gem so that Forem's HTML-to-Markdown pipeline handles code blocks and text nodes in ways the upstream gem does not support: multi-origin language detection for code fences and whitespace normalisation rules that preserve inline code fidelity.

## Scenarios

### Pre block converted to GitHub-flavored fenced code block

1. The converter receives a `<pre>` node and the `github_flavored` configuration flag is enabled.
2. The system inspects the node's CSS class for a `language-<lang>` pattern, then checks the parent element's class for a `highlight-<lang>` pattern, and finally checks the node's class for a Confluence `brush:<lang>;` pattern.
3. The first match found becomes the language identifier appended to the opening fence.
4. If no pattern matches, the opening fence has no language identifier.
5. The output is a fenced code block with the content sandwiched between opening and closing triple-backtick lines.

### Pre block converted to indented code block (non-GitHub-flavored)

1. The converter receives a `<pre>` node and the `github_flavored` flag is disabled.
2. The system ignores language detection entirely.
3. Each line of the block's content is prefixed with four spaces, producing a standard Markdown indented code block.

### br elements inside pre blocks rendered as newlines

1. While processing child nodes of a `<pre>` element, the converter encounters a `<br>` node.
2. The system replaces it with a literal newline character, preserving the visual line break in the resulting code block.

### Text node whitespace normalization

1. The converter receives an HTML text node whose content is not empty after stripping.
2. The system removes any leading or trailing newlines, then replaces all remaining newline, carriage return, and tab characters with spaces, and collapses consecutive spaces into one.
3. Non-breaking space characters (`\u00A0`) are converted to the literal string `&nbsp;` so they survive Markdown rendering.
4. Markdown special characters in the text are escaped, but any escaped characters that appear inside backtick spans are un-escaped to preserve inline code appearance.

### Empty or whitespace-only text node handling

1. The converter receives a text node whose content is blank after stripping.
2. If the node's parent is a list element (`ol` or `ul`), the system returns an empty string to avoid breaking list indentation.
3. If the text is exactly a single regular space, the system preserves that space.
4. Otherwise the system returns an empty string.

## Failures / Exceptions

- Language detection returns `nil` when none of the three CSS class patterns match; the fenced code block is emitted without a language tag, which is valid Markdown.
