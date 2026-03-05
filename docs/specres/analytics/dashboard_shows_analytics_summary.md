---
id: "01KJ6QCRKBRQEYW40CPRAZ1GC7"
name: "dashboard_shows_analytics_summary"
status: "draft"
---

## Related Files

- `app/views/dashboards/_analytics.html.erb` (Template)

## Functional Overview

The analytics summary partial renders a three-card grid on the dashboard, displaying a user's aggregate reactions count, comments count, and page views count. Each metric is formatted with comma delimiters for readability. The page views card applies a special rule: when the view count is 500 or fewer, a localized "less than 500" placeholder string is shown instead of the actual number, deliberately obscuring low-traffic figures.

## Design Intent

The 500-view threshold for displaying exact page views protects authors from seeing discouraging low numbers on new or low-traffic content. Counts above the threshold are shown precisely to reward engagement milestones.

## Key Members

- `@reactions_count` — total public reactions across the user's content
- `@comments_count` — total comments across the user's content
- `@page_views_count` — total page views across the user's content; aliased locally as `num_views` for the threshold check

## Scenarios

### Displaying summary metrics for an active author

1. A signed-in user visits their dashboard.
2. The analytics summary partial is rendered inside the dashboard page.
3. Three metric cards are displayed in a responsive grid: reactions, comments, and page views.
4. The reactions count and comments count are each formatted with comma separators and shown as large, prominent figures.
5. The page views card shows the exact view count with comma formatting.

### Showing a placeholder when page views are 500 or fewer

1. A signed-in user visits their dashboard and their total page views are 500 or fewer.
2. The page views card displays a localized placeholder string (e.g., "< 500") rather than the actual number.
3. The reactions and comments cards still display their real counts normally.

### Showing exact page views when count exceeds 500

1. A signed-in user visits their dashboard and their total page views exceed 500.
2. The page views card displays the exact count formatted with comma delimiters.
