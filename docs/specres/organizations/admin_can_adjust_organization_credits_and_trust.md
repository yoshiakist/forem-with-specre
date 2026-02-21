---
id: "01KJ02MSM04C2X6Q5EEC8T55ZC"
name: "admin_can_adjust_organization_credits_and_trust"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/organizations_controller.rb`
- `spec/requests/admin/organizations_spec.rb` (Test)
- `spec/requests/admin/organizations_baseline_score_spec.rb` (Test)
- `spec/requests/admin/organizations_fully_trusted_spec.rb` (Test)

## Functional Overview

A super-admin can modify three privilege-related attributes of any organization: the credit balance, the fully-trusted flag, and the baseline score. Credits may be added or removed in a specified quantity. The fully-trusted flag is toggled on or off as a boolean. The baseline score is overwritten with a new integer value. All three operations redirect back to the organization's admin show page on success and flash a localized notice. For fully-trusted and baseline-score changes, an audit note is automatically written to the `Note` model whenever the value actually changes, recording who made the change and what it was changed to or from. Credit adjustments always create a note whose content is supplied by the admin in the request.

## Scenarios

### Admin adds or removes credits

1. An admin submits a PATCH request to `update_org_credits` for the target organization, supplying a numeric amount and a `credit_action` of either `add` or `remove`.
2. The system dispatches the appropriate `Credit` class method (`add_to` or `remove_from`) with the organization and the parsed amount.
3. A note is created against the organization using the free-text `note` parameter submitted with the request.
4. The admin is redirected to the organization's admin show page with a localized success notice.

### Admin enables fully-trusted status

1. An admin submits a PATCH request to `update_fully_trusted` with `fully_trusted=true` for an organization that is not currently fully trusted.
2. The organization's `fully_trusted` attribute is set to `true`.
3. Because the status changed, a `Note` is created recording that fully-trusted was enabled, attributed to the current admin.
4. The admin is redirected to the organization's admin show page with a notice indicating the status was enabled.

### Admin disables fully-trusted status

1. An admin submits a PATCH request to `update_fully_trusted` with `fully_trusted=false` for an organization that is currently fully trusted.
2. The organization's `fully_trusted` attribute is set to `false`.
3. Because the status changed, a `Note` is created recording that fully-trusted was disabled, attributed to the current admin.
4. The admin is redirected to the organization's admin show page with a notice indicating the status was disabled.

### Admin updates the baseline score

1. An admin submits a PATCH request to `update_baseline_score` with a new integer value for the target organization.
2. The organization's `baseline_score` attribute is overwritten with the new value.
3. If the score actually changed, a `Note` is created recording the old and new score values, attributed to the current admin.
4. The admin is redirected to the organization's admin show page with a localized success notice.

### Audit note is skipped when value is unchanged

1. An admin submits a request to `update_fully_trusted` or `update_baseline_score` with the same value the organization already holds.
2. The model is updated (no-op in practice), but the comparison detects no change.
3. No `Note` is created, avoiding redundant audit entries.
4. The admin is still redirected with the usual success notice.

## Failures / Exceptions

- If `update_baseline_score` is called with a negative value, `Organization#update!` raises `ActiveRecord::RecordInvalid` due to a model validation; the score is not persisted and the error propagates.
- If an unrecognized `credit_action` value is submitted to `update_org_credits`, `CREDIT_ACTIONS.fetch` raises `KeyError` because no default is provided.
