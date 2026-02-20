---
id: "01KHY7Q0TRBK7YT9F0QKA3FCHP"
name: "emails_batch_custom_send_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/emails/batch_custom_send_worker.rb
- app/controllers/admin/emails_controller.rb
- app/workers/emails/drip_email_worker.rb
- app/workers/emails/enqueue_custom_batch_send_worker.rb
- app/workers/emails/enqueue_digest_worker.rb
- app/workers/emails/remove_old_emails_worker.rb
- app/workers/emails/send_user_digest_worker.rb
- app/workers/emails/survey_daily_email_worker.rb
- spec/workers/emails/batch_custom_send_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Emails::BatchCustomSendWorker` within the emails domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when testing the async call**: Ensures correct behavior under the specified conditions
- **when from_name is passed**: passes from_name through to CustomMailer
- **when from_name is nil (backward compatibility)**: passes from_name through to CustomMailer
- **when the users exist**: Ensures correct behavior under the specified conditions
- **when a user does not exist**: queues the job with the correct arguments regardless of user ID order
- **when subject starts with [TEST]**: queues the job with the correct arguments regardless of user ID order
- **when subject does NOT start with [TEST]**: queues the job with the correct arguments regardless of user ID order

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/emails/batch_custom_send_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/emails_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/emails/drip_email_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_custom_batch_send_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/remove_old_emails_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/send_user_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/survey_daily_email_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: queues the job with the correct arguments regardless of user ID order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** queues the job with the correct arguments regardless of user ID order

### S-2: passes from_name through to CustomMailer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** passes from_name through to CustomMailer

### S-3: passes nil from_name to CustomMailer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** passes nil from_name to CustomMailer

### S-4: sends an email to each user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends an email to each user

### S-5: does not wrap email delivery in a synchronous_commit_off transaction

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not wrap email delivery in a synchronous_commit_off transaction

### S-6: logs an error and continues if one user raises an exception

- **Given** one user raises an exception
- **When** the action is triggered
- **Then** logs an error and continues

### S-7: skips sending any emails

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips sending any emails

### S-8: sends the email regardless of prior email history

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the email regardless of prior email history

### S-9: checks for last email subject and finds none, so sends the email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks for last email subject and finds none, so sends the email

### S-10: sends a new email if the most recent subject started with [TEST]

- **Given** the most recent subject started with [TEST]
- **When** the action is triggered
- **Then** sends a new email

### S-11: skips sending a new email if last email subject does not start with [TEST]

- **Given** last email subject does not start with [TEST]
- **When** the action is triggered
- **Then** skips sending a new email

### S-12: checks the most recent email message (by id) and skips if it doesn

- **Given** it doesn
- **When** the action is triggered
- **Then** checks the most recent email message (by id) and skips

