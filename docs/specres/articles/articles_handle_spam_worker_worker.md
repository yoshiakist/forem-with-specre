---
id: "01KHY7PZMZJMNZYGBGW5WH9X73"
name: "articles_handle_spam_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/handle_spam_worker.rb
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
- spec/workers/articles/handle_spam_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::HandleSpamWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when article exists**: calls Spam::Handler.handle_article! with the article
- **when article does not exist**: calls Spam::Handler.handle_article! with the article
- **when Spam::Handler.handle_article! raises an error**: calls Spam::Handler.handle_article! with the article
- **when article enhancement fails**: calls Spam::Handler.handle_article! with the article
- **integration with content moderation labeling**: calls Spam::Handler.handle_article! with the article
- **when content moderation labeling affects the score**: calls update_score after spam handling
- **when content moderation labeling identifies high quality content**: updates clickbait_score when it

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/handle_spam_worker.rb` -- asynchronous job processing
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

### S-1: calls Spam::Handler.handle_article! with the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls Spam::Handler.handle_article! with the article

### S-2: calls update_score after spam handling

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls update_score after spam handling

### S-3: updates clickbait_score when it

- **Given** the system is in a standard operational state
- **When** it
- **Then** updates clickbait_score

### S-4: does not update clickbait_score when it

- **Given** the system is in a standard operational state
- **When** it
- **Then** does not update clickbait_score

### S-5: does not update clickbait_score when article score is negative after spam handli...

- **Given** the system is in a standard operational state
- **When** article score is negative after spam handling
- **Then** does not update clickbait_score

### S-6: generates and applies tags when conditions are met

- **Given** the system is in a standard operational state
- **When** conditions are met
- **Then** generates and applies tags

### S-7: does not call Spam::Handler.handle_article!

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call Spam::Handler.handle_article!

### S-8: does not raise an error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not raise an error

### S-9: does not call update_score or enhancement

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call update_score or enhancement

### S-10: logs error but continues processing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error but continues processing

### S-11: updates the score with automod_label adjustment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the score with automod_label adjustment

### S-12: updates the score with positive automod_label adjustment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the score with positive automod_label adjustment

