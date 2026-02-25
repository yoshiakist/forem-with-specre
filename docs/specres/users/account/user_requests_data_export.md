---
id: "01KJ9R84BNEKXTFVCSHJ5WNPHY"
name: "user_requests_data_export"
status: "draft"
---

## Related Files

- `app/views/users/_account.html.erb` (Template) — this file participates in multiple behaviors; this card covers only the export section

## Functional Overview

From the account settings page, a user can request an export of their personal data by checking a checkbox and submitting the form. When the export has not yet been requested, the settings page shows a description of the export feature along with the checkbox form. Once the user submits the request, the system marks the user's account with an export-requested flag; on subsequent visits to the account settings page, the export section instead displays a warning notice indicating that the export has already been requested, hiding the form.

## Design Intent

The UI prevents duplicate export requests by switching from a form to an informational notice once a request is recorded. This avoids server-side validation errors and gives the user clear, immediate feedback that their request is pending without requiring them to submit again.

## Scenarios

### User requests a data export for the first time

1. The user navigates to their account settings page.
2. The export section shows a brief description of the export feature and a checkbox labeled for requesting an export.
3. The user checks the checkbox and clicks the submit button.
4. The system records the export request on the user's account (`export_requested` is set to true).
5. On the next page load, the export section displays a warning notice indicating that the export has been requested, and the form is no longer shown.

### User visits the account settings page after already requesting an export

1. The user navigates to their account settings page when an export request is already pending (`export_requested` is true).
2. The export section displays only a warning notice stating that the export has been requested.
3. No form or checkbox is shown; the user cannot submit a duplicate request through this UI.
