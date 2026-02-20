---
id: "01KHY7Q0TD6JCKM6R3M9VSQHY8"
name: "ai_email_digest_summary_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/ai/email_digest_summary.rb
- app/controllers/admin/blocked_email_domains_controller.rb
- app/controllers/admin/email_messages_controller.rb
- app/controllers/admin/emails_controller.rb
- app/controllers/ahoy/email_clicks_controller.rb
- app/controllers/email_authorizations_controller.rb
- app/controllers/email_subscriptions_controller.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/devise_mailer.rb
- spec/services/ai/email_digest_summary_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ai::EmailDigestSummary` within the emails domain.

### Behavioral Areas

- **generate**: generates a summary using AI
- **with validation and retry**: retries once if output contains malformed links with HTML
- **validation edge cases**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/ai/email_digest_summary.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/blocked_email_domains_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/email_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/emails_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/email_authorizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/email_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: generates a summary using AI

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates a summary using AI

### S-2: caches the result

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caches the result

### S-3: is order-independent for caching

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is order-independent for caching

### S-4: depends on article paths for caching

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** depends on article paths for caching

### S-5: returns nil if articles are empty

- **Given** articles are empty
- **When** the action is triggered
- **Then** returns nil

### S-6: returns nil and logs error if AI client fails

- **Given** AI client fails
- **When** the action is triggered
- **Then** returns nil and logs error

### S-7: returns output if valid markdown

- **Given** valid markdown
- **When** the action is triggered
- **Then** returns output

### S-8: retries once if output contains HTML

- **Given** output contains HTML
- **When** the action is triggered
- **Then** retries once

### S-9: retries once if output contains malformed links with HTML

- **Given** output contains malformed links with HTML
- **When** the action is triggered
- **Then** retries once

### S-10: returns nil and logs error if retry also fails

- **Given** retry also fails
- **When** the action is triggered
- **Then** returns nil and logs error

### S-11: accepts valid markdown: #{valid_text.truncate(30).inspect}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid markdown: #{valid_text.truncate(30).inspect}

### S-12: rejects invalid markdown: #{invalid_text.truncate(30).inspect}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid markdown: #{invalid_text.truncate(30).inspect}

