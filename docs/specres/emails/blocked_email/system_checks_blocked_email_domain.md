---
id: "01KJ74FE48B8HJGBTKCFTWECFQ"
name: "system_checks_blocked_email_domain"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/blocked_email_domain.rb`
- `spec/models/blocked_email_domain_spec.rb` (Test)

## Functional Overview

The system provides a class-level `blocked?` method on `BlockedEmailDomain` that determines whether a given domain string is blocked. The check first normalizes the input to lowercase and strips surrounding whitespace, then performs an exact database match against stored blocked domains. If no exact match is found, it additionally checks whether the input domain is a subdomain of any blocked entry by testing whether the input ends with a period-prefixed blocked domain. This means blocking `example.com` automatically blocks `sub.example.com` and any deeper nested subdomains. Blank or nil inputs are treated as safe and return false immediately. A companion `domains` class method returns the full list of blocked domain strings as a plain array for callers that need to enumerate all blocked entries.

## Design Intent

Subdomain matching is included because spam actors frequently rotate through subdomains of the same base domain. Blocking only the exact registered domain would allow `spam1.badactor.com`, `spam2.badactor.com`, and so on to bypass the filter. By treating any suffix of the form `.blocked_domain` as a match, a single entry in the blocked list covers an entire domain tree without requiring administrators to enumerate every possible subdomain.

Case-insensitive comparison is used because domain names are case-insensitive by the DNS specification. Users or integrations may supply mixed-case input (`EXAMPLE.COM`, `Example.COM`) that must resolve to the same blocking decision as the lowercase-normalized records stored in the database.

## Key Members

- `BlockedEmailDomain.blocked?(domain)` — Accepts a domain string and returns true if that domain or any of its parent domains appears in the blocked list. Returns false immediately for blank or nil input without querying the database.
- `BlockedEmailDomain.domains` — Returns a plain array of all blocked domain strings currently stored, suitable for callers that need to enumerate or display the full list.

## Scenarios

### Exact match is detected as blocked

1. The caller provides a domain string that exactly matches an entry in the blocked domains table (e.g., `"example.com"`).
2. The system normalizes the input to lowercase and checks for a direct database record with that domain value.
3. The system returns true.

### Subdomain of a blocked domain is detected as blocked

1. The caller provides a domain string whose parent domain is blocked (e.g., `"sub.example.com"` when `"example.com"` is blocked).
2. The system finds no exact match for the full subdomain string.
3. The system then checks whether the input ends with `.example.com` (or any other blocked domain prefixed by a period).
4. A match is found and the system returns true. Deeply nested subdomains such as `"deep.sub.example.com"` are handled the same way.

### Non-blocked domain returns false

1. The caller provides a domain string that is not present in the blocked list and is not a subdomain of any blocked entry.
2. The system finds no exact match and no subdomain match.
3. The system returns false.

### Blank or nil domain returns false without querying

1. The caller provides an empty string or nil as the domain argument.
2. The system detects the blank value at the start of the method.
3. The system returns false immediately without touching the database.

### Lookup is case-insensitive

1. The caller provides a domain string in any case (e.g., `"EXAMPLE.COM"` or `"Sub.Example.COM"`).
2. The system normalizes the input to lowercase before performing any comparison.
3. The normalized value matches against the stored lowercase entries, returning true when the domain or a parent domain is blocked.

## Failures / Exceptions

- A blank string or nil passed to `blocked?` returns false immediately and does not raise an error or perform a database query.
