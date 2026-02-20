---
id: "01KHY7Q0TTMWT1KGDH0N02VVG4"
name: "emails_drip_email_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/emails/drip_email_worker.rb
- app/controllers/admin/emails_controller.rb
- app/workers/emails/batch_custom_send_worker.rb
- app/workers/emails/enqueue_custom_batch_send_worker.rb
- app/workers/emails/enqueue_digest_worker.rb
- app/workers/emails/remove_old_emails_worker.rb
- app/workers/emails/send_user_digest_worker.rb
- app/workers/emails/survey_daily_email_worker.rb
- spec/workers/emails/drip_email_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Emails::DripEmailWorker` within the emails domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/emails/drip_email_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/emails_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/emails/batch_custom_send_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_custom_batch_send_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/remove_old_emails_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/send_user_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/survey_daily_email_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: sends the default template to users with nil onboarding_subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the default template to users with nil onboarding_subforem_id

### S-2: does not wrap email delivery in a synchronous_commit_off transaction

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not wrap email delivery in a synchronous_commit_off transaction

### S-3: sends custom template to users with their own onboarding_subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends custom template to users with their own onboarding_subforem_id

### S-4: uses the stubbed default_id grouping when Subforem.cached_default_id is stubbed

- **Given** the system is in a standard operational state
- **When** Subforem.cached_default_id is stubbed
- **Then** uses the stubbed default_id grouping

### S-5: does not send emails to users registered outside the drip window

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send emails to users registered outside the drip window

### S-6: does not send emails to users unsubscribed or recently emailed

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send emails to users unsubscribed or recently emailed

