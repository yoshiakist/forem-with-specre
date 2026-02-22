---
id: "01KJ1NAGREGYKBPGQDQH99R94F"
name: "author_can_embed_cloud_run_button_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/cloud_run_tag.rb`
- `app/views/liquids/_cloud_run.html.erb` (Template)
- `spec/liquid_tags/cloud_run_tag_spec.rb` (Test)

## Functional Overview

The `{% cloudrun %}` Liquid tag allows authors to embed Google Cloud Run applications as iframes in articles. It accepts any URL matching the `*.run.app` domain pattern (with or without trailing slash). The rendered iframe is 600px tall with lazy loading. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Key Members

- `REGISTRY_REGEXP` — validates URLs ending in `.run.app` (with optional trailing slash)
- `parse_input` — strips whitespace, validates against the regexp, returns the URL verbatim
- `valid_url?` — checks URL against `REGISTRY_REGEXP`

## Scenarios

### Embedding a Cloud Run application

1. Author writes `{% cloudrun https://my-app-12345.us-west1.run.app %}` in article body
2. System validates the URL matches the `.run.app` domain pattern
3. Rendered output is an iframe (600px height, lazy-loaded, border-radius styling) pointing to the Cloud Run URL

### Automatic detection via UnifiedEmbed

1. Author pastes a `*.run.app` URL into the editor
2. `UnifiedEmbed` matches `REGISTRY_REGEXP` and routes to `CloudRunTag`
3. The same iframe embed is rendered

## Failures / Exceptions

- Non-`.run.app` URLs raise `StandardError` with "Invalid Cloud Run URL"
- Malformed or non-URL input is rejected by the regex validation
