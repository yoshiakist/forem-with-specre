---
id: "01KHYASXS334EE0BHKGBNRD4C0"
name: "organization_helper_formats_credit_options"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/organization_helper.rb
- spec/helpers/organization_helper_spec.rb (Test)

## Functional Overview

The OrganizationHelper provides a view helper method that formats a collection of organizations into HTML select options, displaying each organization's name alongside its unspent credit count for credit allocation interfaces.

## Scenarios

### Helper formats organizations with credit counts for select dropdown

1. The helper receives a collection of organizations.
2. For each organization, the helper generates an option label showing the organization name and unspent credits count (localized).
3. The helper returns HTML option tags suitable for use in a select element, with the organization ID as each option's value.
