---
id: "01KJ7HPV39HXGYWHV2SGNH9R73"
name: "admin_can_view_navigation_links"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/navigation_links_controller.rb`
- `app/models/navigation_link.rb`
- `app/views/admin/navigation_links/index.html.erb` (Template)
- `spec/requests/admin/navigation_link_spec.rb` (Test)

## Functional Overview

When a super-admin visits the navigation links index page, the controller loads all navigation links that belong to the current subforem (or are globally shared) and splits them into two ordered collections: those in the `default` section and those in the `other` section. Both collections are sorted by position ascending, then by name ascending, and are handed to the index template, which renders them in separate tables. The page is protected by the standard admin authentication layer, so only authenticated super-admins can access it.

## Design Intent

Splitting links into `default` and `other` sections lets site operators maintain a primary navigation set separately from supplementary links without mixing them in a single flat list. Scoping by subforem allows multi-tenant installations to show context-appropriate navigation without duplicating records.

## Key Members

- `@default_nav_links` — ordered `NavigationLink` records belonging to the `default` section for the current subforem
- `@other_nav_links` — ordered `NavigationLink` records belonging to the `other` section for the current subforem
- `NavigationLink.from_subforem` — scope that filters links to the current subforem or globally shared ones (`subforem_id` is nil)
- `NavigationLink.ordered` — scope that sorts by `position` ascending, then `name` ascending

## Scenarios

### Admin views the navigation links index

1. An authenticated super-admin navigates to the admin navigation links page.
2. The controller queries navigation links scoped to the current subforem, separated into `default` and `other` sections, each ordered by position then name.
3. The page renders successfully (HTTP 200) and displays both link lists with their name, URL, icon, section, position, and display-to setting.

## Failures / Exceptions

- Unauthenticated or non-admin requests are rejected by the `Admin::ApplicationController` authentication layer before the action runs.
