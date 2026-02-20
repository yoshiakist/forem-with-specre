---
id: "01KHY7Q0SVRC41HG6XGYYFN53D"
name: "blocked_email_domain_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/blocked_email_domains_controller.rb
- app/models/blocked_email_domain.rb
- app/models/email.rb
- app/models/email_authorization.rb
- app/models/email_message.rb
- spec/models/blocked_email_domain_spec.rb

## Functional Overview

This specification defines the expected behavior of `BlockedEmailDomain` within the emails domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **normalization**: Ensures correct behavior under the specified conditions
- **.blocked?**: Ensures correct behavior under the specified conditions
- **.domains**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/blocked_email_domains_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/blocked_email_domain.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email_authorization.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email_message.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: validates presence of domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates presence of domain

### S-2: validates uniqueness of domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates uniqueness of domain

### S-3: validates domain format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates domain format

### S-4: accepts valid domains

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid domains

### S-5: normalizes domain to lowercase

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** normalizes domain to lowercase

### S-6: strips whitespace from domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** strips whitespace from domain

### S-7: returns true for exact matches

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true for exact matches

### S-8: returns true for subdomain matches

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true for subdomain matches

### S-9: returns false for non-blocked domains

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false for non-blocked domains

### S-10: returns false for blank or nil domains

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false for blank or nil domains

### S-11: is case insensitive

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is case insensitive

### S-12: returns array of blocked domains

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns array of blocked domains

