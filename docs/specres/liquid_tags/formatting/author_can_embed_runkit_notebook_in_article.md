---
id: "01KJ1FBXXXWHBNMKZ9HBS5AR6V"
name: "author_can_embed_runkit_notebook_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/runkit_tag.rb`
- `app/views/liquids/_runkit.html.erb` (Template)
- `spec/liquid_tags/runkit_tag_spec.rb` (Test)

## Functional Overview

An article author can embed an interactive RunKit JavaScript notebook directly inside article content by using the `{% runkit %}` Liquid block tag. The tag accepts an optional preamble expression (inline JavaScript code that executes before the main notebook content) as its argument, and the tag body holds the main notebook source code. At render time the tag produces an HTML structure that the RunKit client-side library transforms into a live, runnable notebook widget.

## Design Intent

RunKit notebooks require two separate code regions: a hidden preamble that runs silently before the visible source, and the main source displayed to the reader. The server renders these two regions into hidden `<code>` elements inside a `runkit-element` container. A small inline JavaScript snippet, exposed via `RunkitTag.script`, is loaded once per page; it detects any `.runkit-element` nodes, dynamically loads the RunKit embed library from `//embed.runkit.com`, and then calls `RunKit.createNotebook` to replace each container with a live iframe widget. This lazy, interval-based loading approach avoids a hard dependency on the RunKit CDN at page-load time.

HTML entities in the preamble are unescaped before being written into the hidden code block so that the RunKit library receives plain source text rather than entity-encoded characters. The block body is parsed through Nokogiri to strip any incidental HTML wrapping that Liquid may introduce, ensuring only raw text reaches the notebook.

## Key Members

- `preamble` — optional inline JavaScript snippet passed as the tag argument; sanitized before use and written into the first hidden `<code>` block
- `parsed_content` — the tag body text after HTML-parsing and stripping; written into the second hidden `<code>` block as the main notebook source
- `PARTIAL` (`"liquids/runkit"`) — the Rails partial path used to render the `_runkit.html.erb` template
- `SCRIPT` — a frozen JavaScript string that activates RunKit on any `.runkit-element` node found on the page; exposed via `RunkitTag.script` for inclusion in the page layout

## Scenarios

### Embedding a notebook with preamble and main source

1. The author writes a `{% runkit <preamble_code> %}` block in the article body, where `<preamble_code>` is a JavaScript expression and the block body contains the main notebook source.
2. During article rendering, `RunkitTag#initialize` sanitizes the preamble argument, stripping all HTML tags and rejecting any markup that contains `">` sequences.
3. `RunkitTag#render` parses the block body through an HTML parser to extract plain text, then renders the `liquids/runkit` partial with both `preamble` and `parsed_content` locals.
4. The rendered HTML contains a `<div class="runkit-element">` with two hidden `<code>` blocks: the first holds the unescaped preamble, the second holds the main source.
5. When the page loads in the browser, `activateRunkitTags` detects the `.runkit-element` container, dynamically loads the RunKit embed library, and calls `RunKit.createNotebook` with `preamble` and `source` extracted from the two code blocks.
6. The container is replaced by a live, runnable RunKit notebook iframe.

### Embedding a notebook without a preamble

1. The author writes a `{% runkit %}` block with no tag argument, placing only the main source in the block body.
2. The preamble is sanitized to an empty string.
3. Rendering proceeds identically to the scenario above; the first hidden code block is empty and the RunKit library uses an empty preamble.

### Skipping activation when no runkit elements are present

1. The page does not contain any `.runkit-element` nodes.
2. `areAnyRunkitTagsPresent` returns false and `activateRunkitTags` returns immediately without loading the RunKit library or starting the polling interval.

### Skipping re-activation of an already-active notebook

1. A `.runkit-element` container already has a child `<iframe>` (the RunKit widget has previously been created).
2. `isRunkitTagAlreadyActive` returns true for that element and `replaceTagContentsWithRunkitWidget` skips it, preventing duplicate notebooks.

## Failures / Exceptions

- If the preamble markup contains the sequence `">`, `sanitized_preamble` raises a `StandardError` with the I18n message at key `liquid_tags.runkit_tag.runkit_tag_is_invalid`, preventing potential XSS via attribute-injection in the preamble.
- If the RunKit embed library is unavailable or throws during notebook creation, the `setInterval` callback catches the error, logs it via `console.error`, and clears the polling interval, leaving the hidden code blocks visible as a fallback.
