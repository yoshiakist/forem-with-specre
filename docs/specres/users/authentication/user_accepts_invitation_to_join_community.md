---
id: "01KJVJ43WCHFB50B2K9KC6CVS0"
name: "user_accepts_invitation_to_join_community"
status: "draft"
---

## Related Files

- `app/controllers/invitations_controller.rb`
- `app/views/devise/invitations/edit.html.erb` (Template)
- `spec/requests/invitations_spec.rb` (Test)

## Functional Overview

When an invited user clicks the acceptance link from an invitation email, they land on a form where they set their display name and password. Submitting the form triggers `InvitationsController#update`, which validates the invitation token via Devise Invitable, then marks the user as registered (setting `registered_at` to the current timestamp and `registered` to true), updates their name, and signs them in. If the acceptance fails due to validation errors, the form is re-rendered with the original invitation token preserved so the user can correct their input and resubmit.

## Design Intent

The controller extends `Devise::InvitationsController` rather than reimplementing it from scratch, following the standard Devise override pattern (similar to `OmniauthCallbacksController`). Forem-specific fields (`registered_at`, `registered`, `name`) are updated in a post-acceptance hook after Devise's own `accept_resource` call, keeping the Devise contract intact while layering community-specific onboarding state on top.

## Scenarios

### User successfully accepts invitation and is signed in

1. User opens the invitation email and clicks the acceptance link containing a one-time `invitation_token`.
2. The system renders the invitation edit page showing the community welcome message, a name field, and password/confirmation fields.
3. User fills in their display name, sets a password, and submits the form.
4. The controller calls `accept_resource`, which validates the token and saves the password via Devise Invitable.
5. If no errors occur, the system updates the user record with `registered: true`, `registered_at: Time.current`, and the submitted `name`.
6. The user is signed in immediately and redirected to `after_accept_path_for(resource)`.

### Acceptance fails due to validation errors

1. User submits the invitation form with invalid data (e.g., mismatched passwords or a blank name).
2. `accept_resource` returns errors on the resource.
3. The controller restores `resource.invitation_token` to the raw token from the request so the form can resubmit with the token intact.
4. The invitation edit form is re-rendered displaying the validation error messages.

### User accepts invitation on a private Forem instance

1. An invited user follows the acceptance link even though the Forem is configured as private (not publicly accessible).
2. The invitation acceptance page renders normally — the private-Forem registration gate does not intercept or redirect the request.
3. The user can complete account setup as in the normal acceptance flow.

## Failures / Exceptions

- If the invitation token is invalid or expired, Devise Invitable's `accept_resource` sets errors on the resource, causing the edit form to re-render with the preserved token.
- If `allow_insecure_sign_in_after_accept` is disabled on the resource class, the user is redirected to the sign-in page instead of being signed in automatically after acceptance.
