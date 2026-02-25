---
id: "01KJ9G0HP7SZ3CFPBD2ZW5RR7C"
name: "admin_revokes_user_invitation"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/invitations_controller.rb`
- `app/views/admin/users/index/_invitation_actions_dropdown.html.erb`
- `spec/requests/admin/invitations_spec.rb` (Test)

## Functional Overview

An admin can permanently revoke a pending user invitation by deleting the associated unregistered user record. The admin visits the invitations index where each pending invitee has a dropdown action menu. Selecting "Cancel" triggers a DELETE request to the invitations endpoint. The controller locates the user among those who have not yet registered, destroys the record, and sets a flash message confirming success or reporting validation errors before redirecting back to the invitations list.

## Design Intent

The behavior is scoped exclusively to unregistered users (`registered: false`) to prevent accidental deletion of active accounts. Treating an invitation as a not-yet-registered user record means no separate invitation model is needed; deletion of the record is the canonical way to revoke access.

## Scenarios

### Admin successfully revokes a pending invitation

1. An admin navigates to the pending invitations list.
2. The admin opens the action dropdown next to the target invitee's email address.
3. The admin clicks the "Cancel" button, which sends a DELETE request for that invitee.
4. The system finds the matching unregistered user record and destroys it.
5. A success flash message containing the invitee's email is displayed and the admin is redirected to the invitations index.

### Invitation cannot be destroyed due to an error

1. The admin requests deletion of a pending invitation.
2. The system locates the unregistered user record but the destroy operation fails (e.g., a callback or validation prevents it).
3. The system sets a danger flash message listing the error details.
4. The admin is redirected back to the invitations index without the record being removed.

## Failures / Exceptions

- If the target user is not found among unregistered users (e.g., already registered or does not exist), an `ActiveRecord::RecordNotFound` error is raised and handled by Rails' standard exception pipeline.
- If `destroy` returns false, the controller reads `errors_as_sentence` from the user object and surfaces it as a danger flash message.
