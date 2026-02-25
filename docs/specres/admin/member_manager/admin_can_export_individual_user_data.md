---
id: "01KJ9NBZF1SQAR7DFKTNVZKDYG"
name: "admin_can_export_individual_user_data"
status: "in-development"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `spec/requests/admin/users_spec.rb` (Test)

## Functional Overview

An admin can trigger an asynchronous export of a specific user's content data. When the export is requested, the system determines where to send the resulting file: either to the platform's admin contact email or directly to the user's own email. The export job is enqueued via `ExportContentWorker`, and the admin is immediately redirected back to the user's admin page with a flash message indicating who will receive the export.

## Design Intent

Routing the export to the admin contact email supports GDPR and data-request workflows where an admin needs to review the data before forwarding it to the user. Sending directly to the user's email supports self-service data portability flows. The `send_to_admin` flag makes the destination explicit and auditable at the call site.

## Key Members

- `params[:id]` — identifies the user whose data is to be exported
- `params[:send_to_admin]` — boolean string; when true the export email goes to the platform's admin contact address, when false it goes to the user's own email
- `ExportContentWorker` — background job that performs the actual data export and sends the email
- `ForemInstance.contact_email` — the platform-wide admin contact address used when `send_to_admin` is true

## Scenarios

### Export sent to admin contact email

1. Admin navigates to a user's admin page and triggers the export, selecting the "send to admin" option.
2. The system resolves the destination as the platform's admin contact email (`ForemInstance.contact_email`) and sets the receiver label to `"admin"`.
3. `ExportContentWorker` is enqueued with the user's ID and the admin contact email.
4. The admin is redirected to the user's admin page with a success flash message stating the export was sent to the admin.

### Export sent to user's own email

1. Admin navigates to a user's admin page and triggers the export, selecting the "send to user" option.
2. The system resolves the destination as the user's registered email address and sets the receiver label to `"user"`.
3. `ExportContentWorker` is enqueued with the user's ID and the user's email.
4. The admin is redirected to the user's admin page with a success flash message stating the export was sent to the user.

## Failures / Exceptions

- If the user record cannot be found by `params[:id]`, the request raises a standard ActiveRecord `RecordNotFound` error, resulting in a 404 response (handled by the application's default error handling).
