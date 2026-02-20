---
id: "01KHYAF86G3QF0BH04P5YBJ4EE"
name: "organization_tag_renders_embedded_profile_card"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/organization_tag.rb
- app/views/organizations/_liquid.html.erb
- spec/liquid_tags/organization_tag_spec.rb (Test)

## Functional Overview

The OrganizationTag is a Liquid template tag that allows embedding organization profile cards in article content. It resolves an organization by slug, decorates it for color theming, and renders a card partial with profile image, name, summary, and follow button. Registered as both `{% organization %}` and `{% org %}`.

## Scenarios

### Tag renders organization profile card from slug

1. The author writes `{% organization <slug> %}` or `{% org <slug> %}` in article content.
2. The system strips the app URL prefix and whitespace from the input to extract the slug.
3. The system looks up the Organization by slug.
4. The system decorates the organization for color presentation and generates follow button and color data.
5. The system renders the `organizations/liquid` partial with the organization's profile image, name, slug link, summary, and a follow button.
6. The card is styled with a border and box-shadow using the organization's `darker_color`.

### Tag rejects invalid slug

1. If no organization matches the provided slug, the system raises a StandardError with an "invalid slug" message.
