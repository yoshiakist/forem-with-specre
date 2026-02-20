---
id: "01KHYB21QD394ZG8HWV7KERR60"
name: "organization_profile_dropdown_renders_menu"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/javascript/packs/organizationDropdown.js

## Functional Overview

The organization profile dropdown pack initializes a dropdown menu on the public organization profile page. It uses the shared dropdown utility and dynamically injects a "Report Abuse" link into the dropdown menu via JavaScript to avoid SEO penalties from empty anchor tags in the HTML source.

## Scenarios

### Dropdown initializes on page load

1. The script locates the `.profile-dropdown` element on the page.
2. If the element is missing, initialization is skipped.
3. If the dropdown has already been initialized (tracked via `data-dropdown-initialized`), initialization is skipped to prevent duplicate setup.
4. The script initializes the dropdown toggle between the `organization-profile-dropdown` trigger button and the `organization-profile-dropdownmenu` content.

### Report abuse link is injected dynamically

1. After dropdown initialization, the script finds the `.report-abuse-link-wrapper` element inside the dropdown.
2. The script reads the abuse report URL from the wrapper's `data-path` attribute.
3. The script injects an anchor tag with the URL and "Report Abuse" text into the wrapper's innerHTML.
4. This dynamic injection is used instead of static HTML to avoid SEO crawlers flagging the link as useless.
