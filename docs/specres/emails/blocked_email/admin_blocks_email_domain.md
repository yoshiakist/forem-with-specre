---
id: "01KJ74CHA3SNK2FRMDYG1B7QA5"
name: "admin_blocks_email_domain"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/blocked_email_domains_controller.rb`
- `app/models/blocked_email_domain.rb`
- `app/views/admin/blocked_email_domains/new.html.erb`
- `spec/models/blocked_email_domain_spec.rb` (Test)
- `spec/factories/blocked_email_domains.rb` (Test)

## Functional Overview

An admin can block an email domain by navigating to the new blocked email domain form and submitting a domain name. The system validates that the domain is present, unique, and matches a valid domain format (RFC-compatible label structure with at least one dot-separated TLD of two or more characters). Before saving, the domain is normalized to lowercase and stripped of surrounding whitespace to ensure consistent storage. On success, the admin is redirected to the index listing with a confirmation notice. On failure, the form is re-rendered with validation errors displayed inline.

## Design Intent

Domain normalization happens at the model level via a `before_validation` callback so that uniqueness checks and comparisons always operate on a canonical lowercase form, regardless of how the admin typed the value.

## Key Members

- `domain` — the domain string to block (e.g., `example.com`); normalized to lowercase and stripped before validation

## Scenarios

### Admin successfully blocks a new domain

1. Admin visits the "Add New Blocked Email Domain" page.
2. Admin types a valid domain name (e.g., `example.com`) into the domain field and submits the form.
3. The system normalizes the domain to lowercase and trims whitespace, then saves it.
4. Admin is redirected to the blocked email domains index with a success notice.

### System rejects an invalid domain format

1. Admin submits a value that does not conform to a valid domain structure (e.g., `invalid`, `example..com`, or `example@com`).
2. The system fails validation with the message "must be a valid domain".
3. The form is re-rendered showing the error; no record is created.

### System rejects a duplicate domain

1. Admin attempts to add a domain that already exists in the blocked list.
2. The system fails the uniqueness validation with "has already been taken".
3. The form is re-rendered showing the error; no duplicate record is created.

### System normalizes domain casing and whitespace on save

1. Admin submits a domain with uppercase letters (e.g., `EXAMPLE.COM`) or surrounding spaces (e.g., `  example.com  `).
2. Before validation, the system converts the value to lowercase and strips whitespace.
3. The normalized value (e.g., `example.com`) is persisted.

## Failures / Exceptions

- Blank domain: blocked by presence validation — "can't be blank".
- Invalid format: blocked by format validation — "must be a valid domain". Triggers for single-label names, consecutive dots, trailing dots, and `@`-containing strings.
- Duplicate domain: blocked by uniqueness validation — "has already been taken". Uniqueness is evaluated against the already-normalized stored value.
