---
id: "01KHY7Q0T335WDZDYDV11T14YQ"
name: "email_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/blocked_email_domains_controller.rb
- app/controllers/admin/email_messages_controller.rb
- app/controllers/admin/emails_controller.rb
- app/controllers/ahoy/email_clicks_controller.rb
- app/controllers/email_authorizations_controller.rb
- app/controllers/email_subscriptions_controller.rb
- app/models/blocked_email_domain.rb
- app/models/email.rb
- app/models/email_authorization.rb
- app/models/email_message.rb
- app/sanitizers/comment_email_scrubber.rb
- app/services/ai/email_digest_summary.rb
- app/services/email_digest.rb
- app/services/email_digest_article_collector.rb
- app/validators/email_safe_html_validator.rb
- spec/models/email_spec.rb

## Functional Overview

This specification defines the expected behavior of `Email` within the emails domain.

### Behavioral Areas

- **Associations**: Ensures correct behavior under the specified conditions
- **Callbacks**: Ensures correct behavior under the specified conditions
- **deliver_to_users**: registers #deliver_to_users as an after_commit callback
- **when type_of equals**: Ensures correct behavior under the specified conditions
- **when status is not**: updates the email status to 
- **when status is changed from**: updates the email status to 
- **deliver_to_test_emails**: Ensures correct behavior under the specified conditions
- **when a list of addresses is provided**: falls back to using test_email_addresses and enqueues a job

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/blocked_email_domains_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/email_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/emails_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/email_authorizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/email_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/blocked_email_domain.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email_authorization.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email_message.rb` -- data persistence, validations, and associations
- `app/sanitizers/comment_email_scrubber.rb`
- **Service layer**: `app/services/ai/email_digest_summary.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: registers #deliver_to_users as an after_commit callback

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** registers #deliver_to_users as an after_commit callback

### S-2: does not enqueue any jobs to EnqueueCustomBatchSendWorker

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue any jobs to EnqueueCustomBatchSendWorker

### S-3: does not enqueue any jobs to EnqueueCustomBatchSendWorker

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue any jobs to EnqueueCustomBatchSendWorker

### S-4: enqueues jobs to EnqueueCustomBatchSendWorker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues jobs to EnqueueCustomBatchSendWorker

### S-5: only enqueues once even if re-saved

- **Given** re-saved
- **When** the action is triggered
- **Then** only enqueues once even

### S-6: updates the email status to 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the email status to 

### S-7: enqueues a job with the matching users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues a job with the matching users

### S-8: falls back to using test_email_addresses and enqueues a job

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to using test_email_addresses and enqueues a job

### S-9: does not enqueue any jobs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue any jobs

### S-10: does not enqueue any jobs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue any jobs

