---
id: "01KJ1N6XH2PFHKKE2GJH8ADM1J"
name: "author_can_embed_js_fiddle_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/js_fiddle_tag.rb`
- `app/views/liquids/_jsfiddle.html.erb` (Template)
- `spec/liquid_tags/js_fiddle_tag_spec.rb` (Test)

## Functional Overview

The `{% jsfiddle %}` Liquid tag allows authors to embed JSFiddle code snippets in articles. The tag accepts a jsfiddle.net URL and optional tab display options (`js`, `html`, `css`, `result` — comma-separated). The fiddle is rendered as an iframe at a fixed height of 600px. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Scenarios

### Embedding a JSFiddle

1. Author writes `{% jsfiddle https://jsfiddle.net/user/fiddle_id %}` in article body
2. System validates the URL matches jsfiddle.net domain
3. Rendered output is an iframe with the fiddle URL and height of 600px

### Embedding with tab options

1. Author writes `{% jsfiddle https://jsfiddle.net/user/fiddle_id js,html,result %}`
2. System validates options match the allowed tab names pattern
3. Valid options are appended to the iframe URL path

## Failures / Exceptions

- Invalid or non-jsfiddle.net URL raises `StandardError`
- If all provided options are invalid (none match the tab pattern), `StandardError` is raised
