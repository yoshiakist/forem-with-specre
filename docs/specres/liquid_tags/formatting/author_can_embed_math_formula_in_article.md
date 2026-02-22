---
id: "01KJ1F9C8WFC974AKEZNQQXCED"
name: "author_can_embed_math_formula_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/katex_tag.rb`
- `app/views/liquids/_katex.html.erb`
- `spec/liquid_tags/katex_tag_spec.rb` (Test)

## Functional Overview

Authors can embed rendered mathematical formulas in articles using the `{% katex %}` Liquid block tag. The tag accepts a LaTeX expression as its body, renders it to HTML via the KaTeX library, and wraps the result in a styled element. By default the formula is rendered as a block-level display element; passing the `inline` option renders it as an inline span. The KaTeX stylesheet is injected into the page only once, even when multiple `{% katex %}` tags appear in the same article. If the LaTeX expression is syntactically invalid, the rendered output contains the KaTeX parse error message rather than raising an exception.

## Design Intent

KaTeX is chosen over MathJax for its fast server-side rendering via ExecJS, keeping the rendering step synchronous and avoiding client-side JavaScript execution for formula display. The single-CSS-injection mechanism (tracked via the `katex_existed` context key) prevents redundant stylesheet `<link>` tags when an article contains multiple math formulas. Separating the inline vs. block rendering decision into a private `inline?` helper keeps the `render` method free of conditional logic around the display mode flag passed to `Katex.render`.

## Key Members

- `KatexTag` — Liquid block tag class registered under the tag name `katex`
- `PARTIAL` — path to the ERB partial (`liquids/katex`) used to produce the final HTML output
- `KATEX_EXISTED` — Liquid context key (`"katex_existed"`) used to track whether the KaTeX CSS has already been emitted for the current render
- `render(context)` — extracts the block body text, renders it with KaTeX, determines whether the CSS should be emitted, and delegates final HTML construction to the Rails partial
- `inline?` — returns `true` when the tag markup includes the word `"inline"`, controlling both the KaTeX `display_mode` flag and the wrapping HTML element

## Scenarios

### Rendering a block-level math formula

1. Author writes `{% katex %}` followed by a valid LaTeX expression and `{% endkatex %}` in the article body.
2. The tag body is extracted as plain text, stripped of any HTML wrapper added by the Liquid parser.
3. The expression is passed to the KaTeX renderer with `display_mode: true` (block mode).
4. The rendered KaTeX HTML is wrapped in a `<div class="katex-element">`.
5. Because no previous `{% katex %}` tag has been rendered in this context, the KaTeX stylesheet `<link>` tag is also included in the output.
6. The `katex_existed` key is set in the Liquid context so subsequent tags know the CSS was already emitted.

### Rendering an inline math formula

1. Author writes `{% katex inline %}` followed by a valid LaTeX expression and `{% endkatex %}`.
2. The `inline` word in the tag markup causes `inline?` to return `true`.
3. The expression is passed to the KaTeX renderer with `display_mode: false` (inline mode).
4. The rendered KaTeX HTML is wrapped in a `<span class="katex-element">` instead of a `<div>`.

### Suppressing duplicate CSS when multiple formulas appear

1. An article contains two or more `{% katex %}` blocks.
2. The first tag renders and emits the KaTeX `<link>` stylesheet tag, then sets `katex_existed` to `true` in the Liquid context.
3. Each subsequent tag detects that `katex_existed` is already set and omits the stylesheet `<link>` from its output.
4. The final rendered page contains exactly one KaTeX stylesheet reference regardless of how many formulas are present.

### Handling an invalid LaTeX expression

1. Author writes a `{% katex %}` tag whose body contains a syntactically invalid LaTeX expression.
2. The KaTeX renderer raises an `ExecJS::ProgramError`.
3. The exception is rescued and its message (a KaTeX parse error string) is used as the rendered content in place of the formula HTML.
4. The output is still wrapped in the appropriate block or inline element, so the page renders without a server error.

## Failures / Exceptions

- **Invalid LaTeX syntax:** `ExecJS::ProgramError` is caught and the error message is rendered inline, prefixed with `"ParseError: KaTeX parse error: "`. The page does not raise a 500 error.
- **Empty body:** An empty tag body is passed to KaTeX; the renderer produces an empty or minimal output and no error is raised.
