---
id: "01KJ02HF7MPPR66D6DYJ77T3Z5"
name: "author_can_embed_organization_in_article"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/liquid_tags/organization_tag.rb`
- `spec/liquid_tags/organization_tag_spec.rb` (Test)
- `app/views/organizations/_liquid.html.erb` (Template)

## Functional Overview

An author can embed an organization profile card inside an article body by using the `{% organization <slug> %}` or `{% org <slug> %}` Liquid tag. When the tag is processed, the system looks up the organization by its slug, renders a styled card that includes the organization's profile image, name, summary, and a follow button, and injects the resulting HTML into the article. If the provided slug does not match any known organization, an error is raised and rendering is aborted.

## Scenarios

### Embedding an organization by slug

1. Author writes `{% organization my-org %}` (or `{% org my-org %}`) in the article body.
2. The Liquid tag parser passes the input string to `OrganizationTag`.
3. The tag strips any leading base URL from the input and looks up the organization by its slug.
4. The found organization is rendered into an HTML card via the `organizations/liquid` partial, including its profile image, name, summary, and a follow button styled with the organization's brand colors.
5. The rendered HTML card is inserted at the position of the tag in the article.

### Embedding an organization using a full URL instead of a bare slug

1. Author pastes the full organization URL (e.g., `https://example.com/my-org`) as the tag input.
2. The base URL prefix is stripped automatically, leaving only the slug `my-org`.
3. Processing continues as in the standard slug flow, and the card renders correctly.

### Rejecting an unrecognized slug

1. Author writes `{% organization unknown-slug %}` where `unknown-slug` does not match any organization.
2. The tag attempts to find the organization by slug and finds no record.
3. A `StandardError` is raised with a localized message indicating the slug is invalid.
4. The article rendering fails and the error is surfaced to the author.

## Failures / Exceptions

- If the slug does not correspond to any existing organization, `parse_slug_to_organization` raises `StandardError` with the message from `liquid_tags.organization_tag.invalid_slug` (i18n key). This prevents partially rendered or broken cards from appearing in published articles.
