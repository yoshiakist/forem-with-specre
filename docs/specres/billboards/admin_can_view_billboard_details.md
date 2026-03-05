---
id: "01KJ6EDVX9WX34H0RYPAW57BXR"
name: "admin_can_view_billboard_details"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/billboards_controller.rb`
- `app/views/admin/billboards/show.html.erb` (Template)
- `spec/requests/admin/billboards_spec.rb` (Test)

## Functional Overview

When an authorized admin navigates to a billboard's detail page, the system loads the specified billboard by its ID and retrieves up to 25 of its most recent engagement events — excluding impressions and events with no associated user — ordered from newest to oldest with user associations eager-loaded. The page renders the full set of billboard configuration attributes (name, body content, placement, targeting, approval status, and so on), a live rendered preview of the billboard, aggregate performance statistics (impressions count, clicks count, success rate), and a chronological list of recent user-linked events such as clicks, signups, and conversions.

## Design Intent

Impressions are excluded from the event feed because they are high-volume and not individually actionable; the aggregate impressions count field already surfaces that data. Filtering out events with a nil user prevents the activity list from showing anonymous interactions that cannot be attributed to a specific account. The limit of 25 events keeps the page lightweight while still providing meaningful recent activity.

## Scenarios

### Admin views a billboard's details

1. An authorized admin requests the show page for a specific billboard by its ID.
2. The system locates the billboard record and loads up to 25 recent engagement events (clicks, signups, conversions) that are associated with a real user, ordered most-recent first.
3. The page renders the billboard's full configuration — including name, body content, render mode, template, placement area, targeting rules, published/approved/priority flags, and type.
4. A live rendered preview of the billboard is shown alongside aggregate performance metrics: impressions count, clicks count, and success rate.
5. The recent event activity list shows each event's category, the username of the user who triggered it, and the timestamp.

### Admin navigates to the edit page from the detail view

1. The admin is viewing the billboard detail page.
2. The admin clicks the "Edit" link displayed in the page header.
3. The system redirects the admin to the edit form for the same billboard.

### Geolocation targeting is shown when the feature flag is enabled

1. The geolocation feature flag is enabled for the instance.
2. An admin views the detail page of a billboard with target geolocations configured.
3. The page renders a "Target Geolocations" field displaying the configured regions in ISO 3166 format.

### Role-based targeting fields appear only for logged-in targeting

1. An admin views the detail page of a billboard configured to display only to logged-in users.
2. The page renders "Target Role Names" and "Exclude Role Names" fields showing the configured role filters.
3. These fields are not rendered when the billboard targets all users or only logged-out users.
