---
id: "01KJ7FGSTVKC2DR8D64BF0DMF4"
name: "admin_views_user_activity_stats_on_profile"
status: "draft"
---

## Related Files

- `app/views/admin/users/show/overview/_stats.html.erb` (Template)

## Functional Overview

When an admin views a user's profile in the admin panel, a stats card is rendered showing six key activity metrics for that user: comments count, articles (posts) count, reactions count, followers count, following count, and badge achievements count. Each metric is displayed as a prominent number with a localized label beneath it, arranged in a responsive grid that shows two rows of three columns on smaller screens and a single row of six columns on large screens.

## Scenarios

### Admin views complete activity stats for a user

1. Admin navigates to the user's profile overview page in the admin panel.
2. The system reads six activity counters from the user record: comments count, articles count, reactions count, followers count, following users count, and badge achievements count.
3. The stats section renders each counter as a bold, large-font number paired with a localized label (Comments, Posts, Reactions, Followers, Following, Badges).
4. All six stats are presented side by side in a single-row grid on large screens, providing a quick at-a-glance summary of the user's engagement.

### Admin views stats on a smaller screen

1. Admin opens the user's overview page on a medium or small viewport.
2. The responsive grid collapses from a single six-column row into two rows of three columns.
3. All six stat items remain visible and legible, with their counts and labels still clearly displayed.

### Admin views stats for a new or inactive user

1. Admin opens the overview page for a user who has no posts, comments, reactions, followers, following, or badges.
2. The system renders each counter as zero.
3. The stats section still renders all six metric slots, showing "0" for every count with the appropriate label, ensuring consistent layout regardless of activity level.
