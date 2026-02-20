---
id: "01KHY7Q03X04T5J3XGQGGZ4PZP"
name: "emails_send_user_digest_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/emails/send_user_digest_worker.rb
- spec/workers/emails/send_user_digest_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Emails::SendUserDigestWorker` within the users domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when there**: send digest email when there are at least 3 hot articles
- **when there**: send digest email when there are at least 3 hot articles
- **with AI summary experiment**: generates and includes smart summary if user has recent presence
- **with force_send: true**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/emails/send_user_digest_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: send digest email when there are at least 3 hot articles

- **Given** the system is in a standard operational state
- **When** there are at least 3 hot articles
- **Then** send digest email

### S-2: does not send email when user does not have email_digest_periodic

- **Given** the system is in a standard operational state
- **When** user does not have email_digest_periodic
- **Then** does not send email

### S-3: does not send email when user is not registered

- **Given** the system is in a standard operational state
- **When** user is not registered
- **Then** does not send email

### S-4: includes billboards

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes billboards

### S-5: creates billboard events when billboards are present

- **Given** the system is in a standard operational state
- **When** billboards are present
- **Then** creates billboard events

### S-6: still delivers email even if billboard event creation raises

- **Given** billboard event creation raises
- **When** the action is triggered
- **Then** still delivers email even

### S-7: does not open a transaction when no billboards are present

- **Given** the system is in a standard operational state
- **When** no billboards are present
- **Then** does not open a transaction

### S-8: selects the paired billboard for the second slot

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** selects the paired billboard for the second slot

### S-9: creates events for both the first and the paired second billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates events for both the first and the paired second billboard

### S-10: generates and includes smart summary if user has recent presence

- **Given** user has recent presence
- **When** the action is triggered
- **Then** generates and includes smart summary

### S-11: does not include smart summary if user has no recent presence

- **Given** user has no recent presence
- **When** the action is triggered
- **Then** does not include smart summary

### S-12: does not include smart summary if user presence is nil

- **Given** user presence is nil
- **When** the action is triggered
- **Then** does not include smart summary

