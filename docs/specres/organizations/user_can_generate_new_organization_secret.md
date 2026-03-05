---
id: "01KHYAPESAA0V3WKK075E59EPH"
name: "user_can_generate_new_organization_secret"
status: "draft"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/models/organization.rb`
- `spec/requests/organizations_update_spec.rb` (Test)

## Functional Overview

An organization admin can regenerate the organization's API secret token through the settings interface. The `generate_new_secret` action in `OrganizationsController` loads the organization, authorizes the action via `OrganizationPolicy#generate_new_secret?` (aliased to `update?`, requiring org admin role), replaces the existing secret with a new 100-character random hex string, saves the record, and redirects the admin back to the organization settings page with a success notice. This allows organizations to rotate their secret if it has been compromised or as a routine security measure.

## Key Members

- `OrganizationsController#generate_new_secret` — the controller action that handles the secret rotation request
- `Organization#generated_random_secret` — generates a 100-character hex string via `SecureRandom.hex(50)`
- `Organization#secret` — the 100-character hex token; validated for exact length of 100 and uniqueness
- `OrganizationPolicy#generate_new_secret?` — aliased to `update?`, requires the current user to be an org admin

## Scenarios

### Admin successfully regenerates the secret

1. An organization admin submits a request to the `generate_new_secret` action.
2. The system loads the organization via `set_organization` and authorizes the action (requires org admin role).
3. `Organization#generated_random_secret` produces a new 100-character hex string.
4. The organization's `secret` attribute is replaced and the record is saved.
5. A success flash notice is set and the admin is redirected to `/settings/organization`.

### Non-admin member attempts to regenerate the secret

1. A user who is a member but not an admin of the organization attempts to regenerate the secret.
2. `OrganizationPolicy#generate_new_secret?` (aliased to `update?`) returns `false`.
3. Pundit raises `NotAuthorizedError` and the action is denied.

## Failures / Exceptions

- If the user is not an admin of the organization, Pundit authorization fails and the request is blocked.
- If the organization is not found by the submitted ID, `set_organization` triggers a 404 response.
