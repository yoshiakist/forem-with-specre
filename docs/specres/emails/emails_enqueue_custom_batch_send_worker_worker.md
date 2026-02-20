---
id: "01KHY7Q0TXERTTRWB3XPBZKXW9"
name: "emails_enqueue_custom_batch_send_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/emails/enqueue_custom_batch_send_worker.rb
- app/controllers/admin/emails_controller.rb
- app/workers/emails/batch_custom_send_worker.rb
- app/workers/emails/drip_email_worker.rb
- app/workers/emails/enqueue_digest_worker.rb
- app/workers/emails/remove_old_emails_worker.rb
- app/workers/emails/send_user_digest_worker.rb
- app/workers/emails/survey_daily_email_worker.rb
- spec/workers/emails/enqueue_custom_batch_send_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Emails::EnqueueCustomBatchSendWorker` within the emails domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when email has an audience segment**: uses the segment scope and enqueues BatchCustomSendWorker for those users
- **when email does not have an audience segment**: uses the segment scope and enqueues BatchCustomSendWorker for those users
- **when email has user_query**: Ensures correct behavior under the specified conditions
- **when there are more users than BATCH_SIZE**: uses the segment scope and enqueues BatchCustomSendWorker for those users
- **when no users match the scope**: uses the segment scope and enqueues BatchCustomSendWorker for those users
- **when in non-production environment**: Ensures correct behavior under the specified conditions
- **when users are suspended or spam**: uses the segment scope and enqueues BatchCustomSendWorker for those users

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/emails/enqueue_custom_batch_send_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/emails_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/emails/batch_custom_send_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/drip_email_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/remove_old_emails_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/send_user_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/survey_daily_email_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: uses the segment scope and enqueues BatchCustomSendWorker for those users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the segment scope and enqueues BatchCustomSendWorker for those users

### S-2: uses the default scope and enqueues BatchCustomSendWorker only for users with ne...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the default scope and enqueues BatchCustomSendWorker only for users with newsletters enabled

### S-3: includes users matching the user query

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes users matching the user query

### S-4: sends multiple batches to BatchCustomSendWorker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends multiple batches to BatchCustomSendWorker

### S-5: does not enqueue any jobs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue any jobs

### S-6: uses BATCH_SIZE = 10

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses BATCH_SIZE = 10

### S-7: excludes those users from the scope

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes those users from the scope

### S-8: filters users based on min_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters users based on min_id

### S-9: filters users based on max_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters users based on max_id

### S-10: filters based on both min_id and max_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters based on both min_id and max_id

### S-11: filters custom query results in Ruby

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters custom query results in Ruby

