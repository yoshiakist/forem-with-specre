---
id: "01KHY7Q0TGBD80R4BXWKV7BPBT"
name: "email_digest_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/email_digest_summary.rb
- app/services/email_digest.rb
- app/services/email_digest_article_collector.rb
- spec/services/email_digest_spec.rb

## Functional Overview

This specification defines the expected behavior of `EmailDigest` within the emails domain.

### Behavioral Areas

- **::send_digest_email**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/email_digest_summary.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/email_digest.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/email_digest_article_collector.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: enqueues Emails::SendUserDigestWorker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues Emails::SendUserDigestWorker

### S-2: performs job inline if community is DEV

- **Given** community is DEV
- **When** the action is triggered
- **Then** performs job inline

