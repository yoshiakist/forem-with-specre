---
id: "01KJ1NAHW37CXP0FHM1SM1GT9H"
name: "author_can_embed_git_pitch_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/git_pitch_tag.rb`
- `app/views/liquids/_gitpitch.html.erb` (Template)
- `spec/liquid_tags/git_pitch_tag_spec.rb` (Test)

## Functional Overview

The `{% gitpitch %}` Liquid tag allows authors to embed GitPitch slide presentations in articles. It accepts a `gitpitch.com` URL (HTTP or HTTPS) and renders it in a 450px iframe. GitPitch is a now-defunct service, but the tag remains for backward compatibility with existing content. The tag is **not** registered with `UnifiedEmbed` (no automatic URL detection).

## Key Members

- `URL_REGEXP` — validates `gitpitch.com/` URLs with alphanumeric path segments
- `parse_link` — strips HTML tags, takes the first whitespace-delimited token, validates against `URL_REGEXP`

## Scenarios

### Embedding a GitPitch presentation

1. Author writes `{% gitpitch https://gitpitch.com/user/repo %}` in article body
2. System validates the URL matches the `gitpitch.com` pattern
3. Rendered output is a 450px iframe loading the GitPitch presentation

## Failures / Exceptions

- Non-gitpitch.com URLs or URLs with special characters in the path raise `StandardError` with an i18n invalid-gitpitch-url message
