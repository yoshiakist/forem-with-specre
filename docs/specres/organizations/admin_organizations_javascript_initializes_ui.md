---
id: "01KHYB1FSJRAWD3J79MJ5ZA141"
name: "admin_organizations_javascript_initializes_ui"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/javascript/packs/admin/organizations.jsx
- app/javascript/packs/admin/organizations/modals.js

## Functional Overview

The admin organizations JavaScript pack initializes the options dropdown on the organization show page and wires up a delegated click listener for modal triggers. The modals module provides a caching mechanism that extracts hidden modal content from the DOM on first use, removes the original to avoid ID conflicts, and displays it via a Preact-based window modal.

## Scenarios

### Entry point initializes dropdown and modal listener

1. The pack initializes a dropdown using the `options-dropdown-trigger` button and `options-dropdown` content.
2. A delegated click listener on the document body invokes the organization modal handler for any click event.

### Modal handler shows cached modal content

1. When a click target has a `data-modal-content-selector` attribute, the handler prevents the default action.
2. The handler extracts the modal title, size, and content selector from the target's dataset.
3. On first invocation for a given selector, the handler queries the DOM for the matching element, caches its innerHTML, and removes the original element to prevent duplicate IDs.
4. On subsequent invocations, the cached HTML content is reused without querying the DOM.
5. The handler passes the cached content, title, and size to the `showWindowModal` utility to render the modal.
6. If the click target does not have a `data-modal-content-selector` attribute, the handler returns immediately without action.
