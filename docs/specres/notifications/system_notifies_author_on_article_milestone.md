---
id: "01KJ15VTEFMF2JWBP9FBB6NCSB"
name: "system_notifies_author_on_article_milestone"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/milestone/send.rb`
- `app/workers/notifications/milestone_worker.rb`
- `app/views/notifications/_milestone.html.erb` (Template)
- `spec/services/notifications/milestone/send_spec.rb` (Test)
- `spec/workers/notifications/milestone_worker_spec.rb` (Test)

## Functional Overview

When an article reaches a significant threshold of views or reactions, the system sends a milestone notification to the article's author. A background job (`Notifications::MilestoneWorker`) receives the milestone type ("View" or "Reaction") and the article ID, looks up the article, and delegates to `Notifications::Milestone::Send`. The service determines the appropriate milestone tier, verifies the notification has not already been sent, and creates a `Notification` record for the author. If the article belongs to an organization, an additional notification is created scoped to that organization. Articles published before 2019-02-25 are excluded from milestone notifications. The notification payload includes article metadata and a randomly selected celebratory GIF ID.

## Key Members

- `type` — milestone category; either `"View"` or `"Reaction"`
- `article` — the `Article` record whose metrics are being evaluated
- View milestones — thresholds at 1,024 / 2,048 / 4,096 / 8,192 / 16,384 / 32,768 / 65,536 / 131,072 / 262,144 / 524,288 / 1,048,576 page views
- Reaction milestones — thresholds at 64 / 128 / 256 / 512 / 1,024 / 2,048 / 4,096 / 8,192 public reactions
- `action` — stored on the `Notification` record in the form `"Milestone::<type>::<threshold>"` (e.g., `"Milestone::View::2048"`)

## Scenarios

### Worker dispatches the notification service

1. A caller enqueues `Notifications::MilestoneWorker` with a milestone type string and an article ID.
2. The worker looks up the article by ID. If the article does not exist, it exits without further action.
3. The worker calls `Notifications::Milestone::Send` with the type and the article object.

### View milestone notification is sent for the first time

1. `Notifications::Milestone::Send` is called with type `"View"` for an article published on or after 2019-02-25.
2. The service identifies the highest view milestone threshold the article's current page-view count has just crossed.
3. The service checks whether a notification for that exact milestone action already exists for the user. Finding none, it proceeds.
4. The service creates a `Notification` record for the article's author with the action `"Milestone::View::<threshold>"`, article metadata, and a random GIF ID.
5. The notification is displayed to the author using the milestone template, which shows the article title, milestone count, and the celebratory GIF.

### Reaction milestone notification is sent for the first time

1. `Notifications::Milestone::Send` is called with type `"Reaction"` for an eligible article.
2. The service identifies the appropriate reaction milestone threshold based on the article's current public reaction count.
3. Finding no prior notification for that milestone, it creates a `Notification` record for the author with the action `"Milestone::Reaction::<threshold>"`.

### Organization co-owner also receives a notification

1. After creating the author's notification, the service checks whether the article is associated with an organization.
2. If an `organization_id` is present, the service creates a second `Notification` record scoped to that organization, with the same milestone action and JSON data.

### Duplicate milestone notification is suppressed

1. `Notifications::Milestone::Send` is called for an article that has already received a notification for the current milestone level.
2. The service finds an existing `Notification` record matching the user, article, and action.
3. No new notification is created; the call returns without side effects.

### Article published before cutoff date is skipped

1. `Notifications::Milestone::Send` is called for an article whose `published_at` is earlier than 2019-02-25.
2. The service detects the article predates the milestone feature cutoff.
3. No notification is created; the call returns immediately.

## Failures / Exceptions

- If the article cannot be found by ID in the worker, processing halts silently (no error raised).
- `Notification.create!` will raise `ActiveRecord::RecordInvalid` if the record fails validation, propagating the error to the caller.
