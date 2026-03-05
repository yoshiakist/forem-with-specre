---
id: "01KJ6QFGJH2SC3WK06ZBHEV3S6"
name: "admin_can_configure_user_analytics"
status: "draft"
---

## Related Files

- `app/views/fields/user_analytics_field/_form.html.erb` (Template)
- `app/views/fields/user_analytics_field/_index.html.erb` (Template)
- `app/views/fields/user_analytics_field/_show.html.erb` (Template)

## Functional Overview

The admin panel exposes a user analytics boolean attribute through a set of Administrate custom field partials. When editing a user record, an admin sees a checkbox that toggles the analytics setting on or off. In the user listing and user detail views, the current value of the attribute is displayed as its string representation. Together these three partials give administrators full read and write access to the user analytics flag within the existing Administrate-based admin UI.

## Scenarios

### Admin enables analytics for a user

1. Admin navigates to the user edit form in the admin panel.
2. The user analytics field is rendered as a labeled checkbox reflecting the current boolean value.
3. Admin checks the checkbox and saves the form.
4. The user's analytics attribute is updated to true.

### Admin disables analytics for a user

1. Admin navigates to the user edit form in the admin panel.
2. The user analytics field checkbox is shown as checked because analytics is currently enabled.
3. Admin unchecks the checkbox and saves the form.
4. The user's analytics attribute is updated to false.

### Admin views the analytics setting in the user listing

1. Admin views the users index page in the admin panel.
2. Each user row displays the analytics field as a plain string representation of the boolean value.

### Admin views the analytics setting on the user detail page

1. Admin opens a specific user's detail view in the admin panel.
2. The user analytics field is displayed as its string representation, allowing the admin to confirm the current setting without editing.
