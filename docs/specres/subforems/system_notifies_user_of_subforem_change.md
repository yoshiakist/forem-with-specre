---
id: "01KHYYG7CT65AXSS0G8M61RW6N"
name: "system_notifies_user_of_subforem_change"
status: "draft"
---

## Related Files

- app/workers/notifications/subforem_change_notification_worker.rb
- app/services/notifications/subforem_change_notification/send.rb
- app/views/notifications/_subforemchange.html.erb (Template)

## Functional Overview

When an article is moved from one subforem to another, the system sends an in-app notification to the article's author. The `SubforemChangeNotificationWorker` Sidekiq job dispatches the work asynchronously. The `Notifications::SubforemChangeNotification::Send` service creates a `Notification` record with rich JSON data containing the article details, old and new subforem names/domains, and the reason for the move. The notification is rendered in the UI showing which article was moved, from which community to which, with special messaging when the destination is the "misc" (open discussion) subforem.

## Scenarios

### System creates a subforem change notification

1. The reassignment service queues a `Notifications::SubforemChangeNotificationWorker` with the article ID, old subforem ID, and new subforem ID
2. The worker finds the article and delegates to `Notifications::SubforemChangeNotification::Send`
3. The send service constructs JSON data including article title/path, old subforem name/domain, new subforem name/domain, and a reason message
4. The notification is created with the mascot account as the notifier and the article author as the recipient

### User views the subforem change notification

1. User opens their notifications
2. The `_subforemchange` partial renders a heading, the article link, and the old/new subforem community names with colored styling
3. If the new subforem is the "misc" subforem, a special notice explains that it is an open discussion space

### Worker handles missing article gracefully

1. If the article has been deleted before the worker runs, the worker returns without error
