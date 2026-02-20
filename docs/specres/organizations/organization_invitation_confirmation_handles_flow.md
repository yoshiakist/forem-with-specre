---
id: "01KHYAZK2NZWKS5R8Z4QAG6G1B"
name: "organization_invitation_confirmation_handles_flow"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/views/organizations/confirm_invitation.html.erb

## Functional Overview

The invitation confirmation page renders a multi-state view that handles organization membership invitation acceptance. It resolves the invitation token to a membership, identifies the inviter, and conditionally displays a confirmation form, a wrong-user warning, a sign-in prompt, or an invalid-token error based on the authentication state and token validity.

## Scenarios

### Valid token with correct signed-in user shows confirmation form

1. The page displays a greeting with the invited user's name.
2. The page identifies the inviter as the earliest non-pending member of the organization.
3. If an inviter is found, the invitation message includes the inviter's name and organization name.
4. If no inviter is found, a generic invitation message is shown with just the organization name.
5. An explanatory card describes what an organization is, referencing the community name from settings.
6. A confirmation button submits a POST form to accept the invitation using the token.

### Valid token with wrong signed-in user shows warning

1. If the signed-in user's ID does not match the membership's user_id, a warning notice is displayed.
2. No confirmation button is shown.

### Valid token with no signed-in user shows sign-in prompt

1. A message instructs the user to sign in first.
2. A sign-in button links to the session page, passing the invitation token as a parameter for post-login redirect.

### Invalid or missing token shows error

1. If the membership cannot be resolved from the token, a danger notice displays an invalid token message.
