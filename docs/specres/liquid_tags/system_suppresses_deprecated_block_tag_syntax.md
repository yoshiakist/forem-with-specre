---
id: "01KJ1NWEZ7S0072F27SHTWFQ91"
name: "system_suppresses_deprecated_block_tag_syntax"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/null_tag.rb`
- `spec/liquid_tags/null_tag_spec.rb` (Test)

## Functional Overview

The `NullTag` replaces Liquid's built-in block tags (`assign`, `break`, `capture`, `case`, `cycle`, `decrement`, `echo`, `for`, `if`, `ifchanged`, `include`, `increment`, `render`, `tablerow`, `unless`) with a tag that immediately raises an error on initialization. This prevents authors from using Liquid's programming constructs in article bodies, limiting the template language to Forem's curated set of embed tags only.

## Design Intent

Liquid is a full template language with control flow, variables, and iteration. Allowing these in user-authored content would create security, performance, and complexity risks. By re-registering each built-in tag name to `NullTag`, Forem ensures that any attempt to use these constructs results in a clear error message rather than silent execution or confusing behavior.

## Key Members

- `NullTag` — inherits `Liquid::Block`; `initialize` raises immediately (no `super` call)
- The `%w[...]` array lists all suppressed tag names
- Each tag is re-registered via `Liquid::Template.register_tag(tag, NullTag)`

## Scenarios

### Author attempts to use a suppressed Liquid tag

1. Author writes `{% if condition %}...{% endif %}` in article body
2. Liquid parser instantiates `NullTag` for the `if` tag
3. `NullTag#initialize` raises `StandardError` with "liquid tag is disabled" message including the tag name
4. The article is not rendered; the author sees the error

## Failures / Exceptions

- Any use of the 15 suppressed tag names raises `StandardError` with an i18n "liquid_tag_is_disabled" message containing the tag name
