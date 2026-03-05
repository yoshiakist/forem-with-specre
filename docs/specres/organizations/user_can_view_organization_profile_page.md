---
id: "01KJ02CRB3BH4Q8986WABZKSG4"
name: "user_can_view_organization_profile_page"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/decorators/organization_decorator.rb`
- `app/helpers/organization_helper.rb`
- `app/javascript/packs/organizationDropdown.js`
- `app/views/organizations/show.html.erb` (Template)
- `app/views/organizations/_header.html.erb` (Template)
- `app/views/organizations/_main_feed.html.erb` (Template)
- `app/views/organizations/_metadata.html.erb` (Template)
- `app/views/organizations/_sidebar.html.erb` (Template)
- `spec/decorators/organization_decorator_spec.rb` (Test)
- `spec/helpers/organization_helper_spec.rb` (Test)
- `spec/system/organization/user_views_an_organization_spec.rb` (Test)

## Functional Overview

When a user visits an organization's profile page, the system renders a two-column layout composed of a branded header, a sidebar, and a main article feed. The header displays the organization's logo, name, tagline, summary, join date, location, and social links, along with a follow button and a dropdown menu containing a "Report Abuse" link injected via JavaScript. The sidebar shows team member avatars (capped at 50, ordered by badge count descending), an organization story, a tech stack section, and aggregate counts of published posts and members. The main feed lists the organization's published articles in reverse chronological order. The `OrganizationDecorator` computes brand colors — falling back to defaults when none are configured — and exposes a `fully_banished?` predicate that always returns `false` since organization banning is not yet implemented. Pages with a non-positive aggregate story score receive `noindex`/`nofollow` meta tags to suppress low-quality content from search engines.

## Design Intent

Brand colors are computed via `OrganizationDecorator#enriched_colors`, which falls back to a hard-coded default palette (`#0a0a0a` / `#ffffff`) when the organization has not set custom hex values. This keeps the page visually consistent regardless of configuration completeness. The "Report Abuse" link is injected by `organizationDropdown.js` rather than rendered in HTML to avoid SEO penalties for links that appear useless to crawlers. The sidebar member list uses a lazy-load avatar pattern with `find_each_respecting_scope` to avoid loading a potentially large number of user records into memory at once.

## Key Members

- `OrganizationDecorator#enriched_colors` — returns a `{ bg:, text: }` hash using the organization's custom hex colors when present, otherwise the default palette
- `OrganizationDecorator#darker_color(adjustment)` — adjusts the brightness of the enriched background color; default adjustment is `0.88`
- `OrganizationDecorator#fully_banished?` — always returns `false`; placeholder for future organization banning functionality
- `OrganizationHelper#orgs_with_credits(organizations)` — builds an HTML `<select>` options list showing each organization's name and unspent credit count
- `@user_limit` — controls the maximum number of member avatars shown in the sidebar (capped at 50)

## Scenarios

### Viewing the organization header

1. A visitor navigates to `/<organization_slug>`.
2. The page title is set to the organization's name.
3. The header renders the organization's logo, name, optional tagline, summary (or a placeholder if blank), join date, optional location, and optional Twitter/GitHub/website links.
4. A "Follow" button is shown; if the visitor is already following the organization, it reads "Following" instead.
5. A dropdown button appears in the header actions area; on activation it reveals a "Report Abuse" link pointing to `/report-abuse?url=<organization_url>`.

### Viewing the sidebar

1. The sidebar lists member avatars ordered by badge count descending, up to a maximum of 50.
2. If the organization has more than 50 members, a "See All Members" link is shown that navigates to `/<slug>/members`.
3. If the organization has a story set, it is rendered in a sidebar card.
4. If the organization has a tech stack set, it is rendered in a sidebar card.
5. The sidebar displays the total count of published posts and total member count.

### Viewing the article feed

1. The main content area lists articles published by the organization, rendered as story cards.
2. Articles are fetched in reverse chronological order via the `index-container` element's data parameters.
3. If no articles have been published yet, the feed area is empty and a loading indicator is present.

### SEO treatment for low-quality pages

1. When the sum of scores across all organization stories is zero or negative, the page head includes `noindex` and `nofollow` meta tags.
2. When at least one story has a positive score, no robots meta tags are added.

### Color theming

1. When an organization has custom `bg_color_hex` and `text_color_hex` values, those are used to compute the `--profile-brand-color` CSS custom property.
2. When no custom colors are set, the decorator falls back to the default dark palette (`#0a0a0a` background, `#ffffff` text).
3. The CSS variable is applied at the `:root` level so all themed elements on the page inherit it.
