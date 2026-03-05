---
id: "01KJ9RB18HTF04ZGD4MHY8BSN1"
name: "author_views_subscriber_dashboard"
status: "draft"
---

## Related Files

- `app/views/dashboards/subscriptions.html.erb` (Template)

## Functional Overview

When an author navigates to their subscriber dashboard for a specific source (such as an article or podcast), the view displays the page title and a heading that identifies the source by name and links to it. If the source has active subscribers, the view renders a table listing each subscriber's display name (linked to their DEV profile), their email address (as a mailto link), and how long ago they subscribed. When there are no subscribers, the view shows an empty-state card instead. Pagination controls appear below the table whenever the subscriber list spans multiple pages.

## Design Intent

The dashboard is scoped to a single source so that authors can distinguish subscribers by content piece. Linking subscriber names to their DEV profiles and exposing subscriber emails as mailto links allows authors to engage directly with their audience from within the dashboard. Pagination uses kaminari-compatible helpers to keep large subscriber lists manageable.

## Scenarios

### Author views dashboard with existing subscribers

1. The author navigates to the subscriptions dashboard for a source that has at least one subscriber.
2. The page title and headings display the source's title with a link to the source.
3. A table renders one row per subscriber, showing the subscriber's name (linked to their DEV profile), their email address (as a mailto link), and the relative time since they subscribed (e.g., "3 days ago").
4. Pagination controls are shown below the table if the subscriber list spans more than one page.

### Author views dashboard with no subscribers

1. The author navigates to the subscriptions dashboard for a source that has no subscribers.
2. The page title and headings display the source's title with a link to the source.
3. No table is rendered; instead, a secondary card is shown with an empty-state message that names the source type (e.g., "article" or "podcast").

### Author navigates between pages of subscribers

1. The author is on the subscriptions dashboard for a source with more subscribers than fit on a single page.
2. The subscriber table shows the first page of results.
3. The author clicks a pagination link to advance to the next page.
4. The table updates to show the next set of subscribers without resetting any other URL parameters.
