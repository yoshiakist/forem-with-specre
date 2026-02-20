---
id: "01KHYAY4DGRYJFMXJ7BBYNVE7Y"
name: "organization_profile_page_displays_public_view"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/views/organizations/show.html.erb
- app/views/organizations/_header.html.erb
- app/views/organizations/_sidebar.html.erb
- app/views/organizations/_metadata.html.erb
- app/views/organizations/_main_feed.html.erb

## Functional Overview

The organization profile page renders a public-facing view composed of a header with branding and social links, a sidebar showing team members and organization details, metadata about company size and contact, and a main feed of published articles. The page conditionally applies noindex/nofollow meta tags based on article score totals and includes JSON-LD structured data for non-signed-in users.

## Scenarios

### Header displays organization identity and actions

1. The header renders the organization's profile image, name, tag line, and summary.
2. If the organization has a location, it is displayed with a location icon.
3. The joined date is displayed using localized date formatting.
4. Social links (Twitter, GitHub, website) are conditionally rendered based on presence.
5. A follow button is displayed with the organization's data info for JavaScript interaction.
6. A dropdown menu provides a report-abuse link for the organization.
7. The header applies a brand color derived from the organization's color settings.
8. For non-signed-in users without internal navigation, JSON-LD structured data is embedded.

### Sidebar shows team members and organization details

1. If the organization has active users, a team section displays profile images up to a configurable limit.
2. If the member count exceeds the limit, an "all members" link directs to the members page.
3. If the organization has a story, it is displayed in a sanitized sidebar card.
4. If the organization has a tech stack, it is displayed in a separate card.
5. Post count and member count statistics are shown in a summary card.

### Metadata displays company information

1. If the organization has an email, it is displayed as a mailto link labeled as support contact.
2. If the organization has a company size, it is displayed.
3. If neither email nor company size is present, the metadata section is omitted.

### Main feed renders published articles

1. The page sets up a data container with parameters for sort order, organization ID, and timeframe filtering.
2. If stories are present, the main feed partial renders each story using the single_story article partial.
3. A loading indicator is displayed for asynchronous article loading.
4. The page includes JavaScript packs for stories list, bookmark buttons, and article date localization.

### SEO controls based on content quality

1. If the total score of stories is not positive, noindex and nofollow meta tags are added.
2. If stories have positive scores, no restrictive meta tags are applied.
