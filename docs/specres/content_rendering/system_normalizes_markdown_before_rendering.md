---
id: "01KJ2X9JEDPKB2DTN1GAMBQ254"
name: "system_normalizes_markdown_before_rendering"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/markdown_processor/fixer/base.rb`
- `app/services/markdown_processor/fixer/fix_all.rb`
- `app/services/markdown_processor/fixer/fix_for_comment.rb`
- `app/services/markdown_processor/fixer/fix_for_preview.rb`
- `app/services/markdown_processor/traverser.rb`
- `spec/services/markdown_processor/fixer/base_spec.rb` (Test)
- `spec/services/markdown_processor/fixer/fix_all_spec.rb` (Test)
- `spec/services/markdown_processor/fixer/fix_for_comment_spec.rb` (Test)
- `spec/services/markdown_processor/fixer/fix_for_preview_spec.rb` (Test)
- `spec/services/markdown_processor/traverser_spec.rb` (Test)

## Functional Overview

Before markdown is rendered, the system applies a series of normalization fixes to ensure the content is well-formed and safe to process. The `MarkdownProcessor::Fixer::Base` class provides a pipeline of fix methods that are applied in sequence to the raw markdown string. Concrete subclasses — `FixAll`, `FixForComment`, and `FixForPreview` — each declare a `METHODS` constant that selects a subset of fixes appropriate for that rendering context. Fixes include: quoting unquoted front-matter `title` and `description` fields, lowercasing the `published` field, normalizing Windows-style line endings to Unix style, splitting space-separated tags into comma-separated form, and escaping underscores in `@username` mentions that would otherwise be interpreted as italic markers by the Markdown renderer. A `Traverser` helper class is used during username escaping to walk the document line by line while tracking whether the current position is inside a fenced code block, so that usernames inside code blocks are intentionally left unescaped.

## Design Intent

The pipeline design (reduce over fix methods) allows each subclass to declare exactly which normalizations are relevant for its rendering context without duplicating logic. Comments in preview mode require fewer fixes than full article rendering, and comment rendering requires only username escaping. This keeps each context's behavior explicit and auditable via the `METHODS` constant. The `Traverser` exists to provide a single, testable abstraction for code-block–aware line iteration, avoiding inline state tracking scattered across fix methods.

## Key Members

- `Base::METHODS` (declared by subclass) — ordered list of fix method names to apply when `.call` is invoked
- `Base::FRONT_MATTER_DETECTOR` — regex matching the `---...---` YAML front-matter block
- `Base::USERNAME_WITH_UNDERSCORE_REGEXP` — regex matching `@_username_` patterns not preceded by a backtick
- `Traverser#in_codeblock?` — returns true when the current line being yielded falls inside a fenced code block

## Scenarios

### Full normalization via FixAll

1. A caller invokes `MarkdownProcessor::Fixer::FixAll.call(markdown)` with raw article markdown.
2. The system applies all six fix methods in order: quoting the `title`, quoting the `description`, lowercasing `published`, converting `\r\n` to `\n`, splitting tag strings into comma-separated form, and escaping underscored usernames outside code blocks.
3. The fully normalized markdown string is returned.

### Front-matter title and description are quoted

1. The fix pipeline detects that the `title` or `description` field in the front matter is not already wrapped in single or double quotes.
2. Any unescaped double quotes within the value are escaped with a backslash.
3. The entire value is then wrapped in double quotes, producing a valid YAML string literal.
4. If the value is already wrapped in quotes (single or double), the field is left unchanged.

### Windows line endings are normalized

1. The fix receives markdown containing `\r\n` (Windows-style) line endings.
2. Every `\r\n` sequence is replaced with `\n`, producing Unix-style line endings throughout.

### Underscored usernames are escaped outside code blocks

1. The fix checks whether the markdown contains any `@_username_` pattern not preceded by a backtick; if none are found, the markdown is returned immediately without further processing.
2. A `Traverser` iterates the markdown line by line. For each line, the traverser determines whether it is inside a fenced code block (delimited by triple backticks).
3. Lines inside a fenced code block, or inline code spans (preceded by a backtick), are skipped without modification.
4. For all other lines, each `@_username_` occurrence has its underscores escaped as `\_`, preventing the Markdown renderer from interpreting them as italic markers.

### Context-specific fix subsets

1. When rendering a comment, `MarkdownProcessor::Fixer::FixForComment.call(markdown)` is used; only the username-underscore escaping fix is applied.
2. When rendering a preview, `MarkdownProcessor::Fixer::FixForPreview.call(markdown)` is used; front-matter title and description quoting plus username escaping are applied, but line-ending conversion, published casing, and tag splitting are omitted.
3. When nil is passed to any fixer, the method returns immediately without error.

## Failures / Exceptions

- If `markdown` is `nil`, `Base.call` returns `nil` immediately and none of the fix methods are invoked.
