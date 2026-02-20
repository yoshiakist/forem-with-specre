---
id: "01KHY7Q0V5YNZKKRVKBGQWEM0Z"
name: "emails_survey_daily_email_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/emails/survey_daily_email_worker.rb
- app/controllers/admin/emails_controller.rb
- app/workers/emails/batch_custom_send_worker.rb
- app/workers/emails/drip_email_worker.rb
- app/workers/emails/enqueue_custom_batch_send_worker.rb
- app/workers/emails/enqueue_digest_worker.rb
- app/workers/emails/remove_old_emails_worker.rb
- app/workers/emails/send_user_digest_worker.rb
- spec/workers/emails/survey_daily_email_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Emails::SurveyDailyEmailWorker` within the emails domain.

### Behavioral Areas

- **when allow_resubmission is false**: Ensures correct behavior under the specified conditions
- **when allow_resubmission is true**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/emails/survey_daily_email_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/emails_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/emails/batch_custom_send_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/drip_email_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_custom_batch_send_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/enqueue_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/remove_old_emails_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/send_user_digest_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: only processes active surveys with daily_email_distributions > 0

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only processes active surveys with daily_email_distributions > 0

### S-2: samples the exact number of eligible users defined in daily_email_distributions ...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** samples the exact number of eligible users defined in daily_email_distributions and ignores users who started/completed it

### S-3: includes users who have already completed the survey

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes users who have already completed the survey

