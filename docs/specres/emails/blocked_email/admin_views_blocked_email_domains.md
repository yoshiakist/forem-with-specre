---
id: "01KJ74BNMR2A3VMTTYP0YK4Q2T"
name: "admin_views_blocked_email_domains"
status: "draft"
---

## Related Files

- `app/controllers/admin/blocked_email_domains_controller.rb`
- `app/views/admin/blocked_email_domains/index.html.erb`

## Functional Overview

The admin index action retrieves all blocked email domain records sorted alphabetically by domain name and renders them in a management page. When domains are present, each entry is displayed with its domain name and the time since it was added, alongside a remove button. When no domains exist, a notice is shown with a link to add the first one. The page also provides a persistent explanation of how blocked domains interact with registration, including subdomain inheritance and co-operation with the Authentication settings.

## Design Intent

Sorting blocked domains alphabetically makes the list scannable for admins managing many entries. The co-existence explanation on the index page ensures admins understand that this list supplements (rather than replaces) the existing "Blocked Registration Email Domains" setting, reducing the risk of misconfiguration.

## Key Members

- `@blocked_email_domains` — collection of all `BlockedEmailDomain` records, ordered ascending by `domain`

## Scenarios

### Admin views a populated list of blocked domains

1. Admin navigates to the blocked email domains admin index page
2. The system queries all blocked email domain records, ordered alphabetically by domain name
3. The page renders a card listing each blocked domain with its name and a human-readable timestamp indicating how long ago it was added
4. Each entry includes a "Remove" button for inline deletion
5. A static informational section explains subdomain inheritance and the relationship with the Authentication settings

### Admin views the index page when no domains are blocked

1. Admin navigates to the blocked email domains admin index page
2. The system queries blocked email domain records and finds none
3. The page renders a warning notice stating that no domains are blocked, with an inline link to the "Add" page
4. The static informational section is still displayed below the notice

## Failures / Exceptions

- No explicit error handling is present in the index action; any database errors would propagate as unhandled exceptions to the default Rails error handler
