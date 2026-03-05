---
id: "01KJ6FEDNZHYXEPQG8RAJDXB3D"
name: "admin_can_view_and_revoke_badge_achievements"
status: "draft"
---

## Related Files

- `app/controllers/admin/badge_achievements_controller.rb`
- `app/models/badge_achievement.rb`
- `app/views/admin/badge_achievements/index.html.erb` (Template)
- `spec/requests/admin/badge_achievements_spec.rb` (Test)
- `spec/models/badge_achievement_spec.rb` (Test)

## Functional Overview

The admin badge achievements interface lets administrators inspect all badge awards across the platform and remove individual awards when necessary. The index action loads badge achievements in reverse chronological order, eager-loading the associated badge and user records, and exposes them through a Ransack-backed search so admins can filter by user ID. Results are paginated at 15 records per page. The destroy action looks up a specific achievement by ID and permanently deletes it, responding with a JSON success message on success or a JSON error message if the deletion fails.

## Scenarios

### Admin views the badge achievements list

1. An authenticated admin navigates to the badge achievements admin page.
2. The system fetches all badge achievements ordered by newest first, with badges and users preloaded.
3. The page renders a paginated table showing each achievement's user ID, username, badge title, and badge image, 15 records per page.
4. A search field is available to filter achievements by user ID.

### Admin searches badge achievements by user ID

1. An authenticated admin enters a user ID into the search field and submits the form.
2. The system applies the filter via Ransack and returns only the achievements belonging to that user.
3. The filtered results are displayed in the same paginated table.

### Admin successfully revokes a badge achievement

1. An authenticated admin clicks the "Remove" button on a badge achievement row.
2. A confirmation modal is displayed before the action is sent.
3. After confirmation, the system sends a DELETE request to the badge achievement endpoint.
4. The system destroys the record and responds with HTTP 200 and a JSON success message.

### Destroy fails due to a persistence error

1. An authenticated admin initiates a DELETE request for a badge achievement.
2. The record is found but cannot be destroyed (for example, due to a callback failure).
3. The system responds with HTTP 422 and a JSON error message.

## Failures / Exceptions

- If `BadgeAchievement#destroy` returns false, the controller renders `{ error: "Something went wrong." }` with status 422.
- The index view includes a notice warning that automatically re-awarded badges will be re-granted even if removed manually.
