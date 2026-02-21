---
id: "01KHZ3WD78QFP2ADRDW1QBJZZN"
name: "admin_can_configure_community_identity"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings/communities_controller.rb`
- `app/models/settings/community.rb`
- `app/lib/constants/settings/community.rb`
- `app/views/admin/settings/forms/_community.html.erb` (Template)
- `spec/models/settings/community_spec.rb` (Test)

## Functional Overview

A super-admin can configure the community's identity settings that appear across the platform. These include the community name, tagline, description, member label (the term used to refer to users), the staff user ID, and the copyright start year. The community name is validated to reject angle brackets (`<`, `>`) to prevent injection. The communities controller inherits from the settings base controller with no custom logic.

## Scenarios

### Admin sets community name and description

1. Admin enters a `community_name` and `community_description`
2. System validates the community name does not contain `<` or `>` characters
3. System persists the values; the community name appears in headers, titles, and meta tags across the platform

### Admin customizes member terminology

1. Admin sets `member_label` to a custom term (e.g., "developer", "contributor")
2. Admin sets `tagline` for the community's one-line description
3. System persists the values; the member label is used throughout the UI to refer to registered users

### Admin assigns staff user and copyright

1. Admin sets `staff_user_id` to the user ID of the designated staff account (the form accepts a username and converts it to an ID via JavaScript)
2. Admin sets `copyright_start_year` to control the footer copyright range
3. System persists the values; defaults are user ID 1 and the current year respectively

## Failures / Exceptions

- Community name containing `<` or `>` is rejected with a validation error
