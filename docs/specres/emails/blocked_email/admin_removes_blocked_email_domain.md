---
id: "01KJ74D0D1M1BE0489HGAP700S"
name: "admin_removes_blocked_email_domain"
status: "draft"
---

## Related Files

- `app/controllers/admin/blocked_email_domains_controller.rb`
- `app/views/admin/blocked_email_domains/index.html.erb`

## Functional Overview

An admin can remove a previously blocked email domain from the system. On the blocked email domains index page, each listed domain has a "Remove" button that triggers a browser confirmation dialog before proceeding. When the admin confirms, a DELETE request is sent to the server, the domain record is destroyed, and the admin is redirected back to the index page with a success notice. If the admin cancels the confirmation dialog, no action is taken.

## Design Intent

The confirmation dialog ("Are you sure you want to remove <domain> from the blocked domains list?") is rendered inline via a `data-confirm` attribute on the remove link, relying on the browser or Rails UJS to intercept and prompt before submission. This prevents accidental removal without requiring a separate confirmation page or modal.

## Scenarios

### Admin removes a blocked domain with confirmation

1. Admin navigates to the Blocked Email Domains admin page, which lists all currently blocked domains in alphabetical order.
2. Admin clicks the "Remove" button next to the domain they want to unblock.
3. A confirmation dialog appears asking "Are you sure you want to remove <domain> from the blocked domains list?".
4. Admin confirms the dialog.
5. The domain record is deleted from the database.
6. Admin is redirected to the blocked email domains index page with the notice "Blocked email domain was successfully removed."
7. The removed domain no longer appears in the list.

### Admin cancels the removal confirmation

1. Admin navigates to the Blocked Email Domains admin page.
2. Admin clicks the "Remove" button next to a domain.
3. A confirmation dialog appears.
4. Admin cancels the dialog.
5. No request is sent to the server; the domain remains in the blocked list and the page stays unchanged.
