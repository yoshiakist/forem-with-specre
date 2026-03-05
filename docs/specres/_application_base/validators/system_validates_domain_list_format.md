---
id: "01KJXNEY6XZP2ZTVKP791AZD5G"
name: "system_validates_domain_list_format"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/validators/valid_domain_csv_validator.rb`
- `spec/validators/valid_domain_csv_validator_spec.rb` (Test)

## Functional Overview

`ValidDomainCsvValidator` is an `ActiveModel::EachValidator` that validates an array of domain strings, ensuring every entry conforms to a standard hostname format. Each domain must begin and end with an alphanumeric character, may include hyphens in the middle, and must have at least one dot-separated suffix of two or more alphabetic characters. If any domain in the array fails this check, an error is added to the attribute using a locale-based message. When the attribute value is `nil` or absent the validator skips without error.

## Design Intent

Although the validator is named "CSV", it operates on an already-coerced array rather than a raw comma-separated string. Upstream callers (e.g., `Authentication::Base`) are responsible for splitting a CSV input into an array before the validator runs. This separation of concerns keeps the validator focused purely on format checking rather than parsing.

## Key Members

- `VALID_DOMAIN` — Regular expression that enforces the hostname format: starts and ends with an alphanumeric character, allows hyphens in the middle (up to 61 characters per label), and requires at least one dot-separated TLD of two or more letters.

## Scenarios

### All domains in the array are valid

1. A model attribute holds an array of one or more domain strings, each matching the standard hostname pattern (e.g., `"hello.com"`, `"seo-hunt.com"`).
2. The validator iterates the array and every domain matches `VALID_DOMAIN`.
3. No error is added and the record is considered valid.

### Array contains at least one invalid domain

1. A model attribute holds an array where one or more entries do not match the hostname pattern (e.g., a bare label with no TLD, or a domain starting with a dash).
2. The validator finds at least one domain that fails the regex check.
3. An error is added to the attribute using the configured message or the default I18n key `validators.valid_domain_csv_validator.invalid_list_format`.

### Attribute value is nil or absent

1. The attribute value is `nil` (not yet set).
2. The validator returns immediately without checking any domains.
3. No error is added.

## Failures / Exceptions

- A domain that starts or ends with a hyphen is rejected.
- A bare hostname with no dot-separated TLD (e.g., `"notadomain"`) is rejected.
- Mixed arrays where some entries are valid and at least one is invalid cause the entire attribute to be marked invalid.
