---
id: "01KHY7PZN4CYCJVXKN1AY5KVDH"
name: "articles_publish_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/publish_worker.rb
- app/controllers/admin/articles_controller.rb
- app/controllers/api/v0/articles_controller.rb
- app/controllers/api/v1/articles_controller.rb
- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/controllers/articles_controller.rb
- app/controllers/concerns/api/articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/pinned_articles_controller.rb
- app/controllers/stories/tagged_articles_controller.rb
- app/helpers/articles_helper.rb
- spec/workers/articles/publish_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::PublishWorker` within the articles domain.

### Behavioral Areas

- **with 2 articles**: schedules Notifications::NotifiableActionWorker twice for 2 articles
- **creating notifications**: calls Slack::Messengers::ArticlePublished to send slack notifications

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/publish_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/articles_helper.rb` -- shared view utility methods


## Scenarios

### S-1: calls Slack::Messengers::ArticlePublished to send slack notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls Slack::Messengers::ArticlePublished to send slack notifications

### S-2: sends notifications to mentioned users and followers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends notifications to mentioned users and followers

### S-3: schedules Notifications::NotifiableActionWorker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** schedules Notifications::NotifiableActionWorker

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-6: schedules Notifications::NotifiableActionWorker twice for 2 articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** schedules Notifications::NotifiableActionWorker twice for 2 articles

### S-7: sends notifications to mentioned users and followers for 2 articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends notifications to mentioned users and followers for 2 articles

### S-8: creates a notification eventually

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification eventually

### S-9: creates a context notification as well

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a context notification as well

### S-10: creates a notification for each article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification for each article

### S-11: creates a ContextNotification for each article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a ContextNotification for each article

