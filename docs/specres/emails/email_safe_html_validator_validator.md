---
id: "01KHY7Q0TKE7SNAA1QC2RMN3ED"
name: "email_safe_html_validator_validator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/validators/email_safe_html_validator.rb
- spec/validators/email_safe_html_validator_spec.rb

## Functional Overview

This specification defines the expected behavior of `EmailSafeHtmlValidator` within the emails domain.

### Behavioral Areas

- **valid HTML**: allows complex but safe HTML
- **invalid HTML**: allows complex but safe HTML
- **edge cases**: handles event handlers with various cases

### Implementation Architecture

The behavior is implemented across the following layers:

- **Validator**: `app/validators/email_safe_html_validator.rb` -- custom input validation rules


## Scenarios

### S-1: allows simple paragraph with inline styles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows simple paragraph with inline styles

### S-2: allows links with inline styles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows links with inline styles

### S-3: allows tables with inline styles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows tables with inline styles

### S-4: allows multiple allowed tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows multiple allowed tags

### S-5: allows images with safe attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows images with safe attributes

### S-6: allows blank/nil values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows blank/nil values

### S-7: rejects JavaScript in script tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects JavaScript in script tags

### S-8: rejects inline JavaScript

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects inline JavaScript

### S-9: rejects event handlers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects event handlers

### S-10: rejects external stylesheets

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects external stylesheets

### S-11: rejects style tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects style tags

### S-12: rejects @import in styles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects @import in styles

