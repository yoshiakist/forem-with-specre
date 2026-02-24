---
id: "01KJ7FFSMG6QWZ7S8QQ26PD1E5"
name: "system_warns_admin_about_outdated_deployment"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/views/admin/overview/_notices.html.erb`
- `app/views/admin/overview/index.html.erb` (Template)
- `spec/requests/admin/overview_spec.rb` (Test)

## Functional Overview

When a super admin visits the admin overview page, the system checks whether the Forem instance has been deployed recently. If the deployment timestamp is older than two weeks, a notice banner is rendered above the overview content urging the admin to re-deploy from the main branch. The severity of the banner escalates from a warning level (yellow) if the deployment is between two and four weeks old, to a danger level (red) if it is more than four weeks old. No notice is shown when the deployment is recent or when no deployment timestamp is recorded.

## Design Intent

The two-tier severity model (warning vs. danger) gives admins a graduated signal: a gentle prompt after two weeks and an urgent alert after four weeks. This reduces the risk of painful re-deployments caused by large accumulated divergence from the main branch.

## Scenarios

### No notice shown for recent deployment

1. The admin visits the overview page while the instance was deployed less than two weeks ago.
2. The notices partial evaluates the deployment timestamp and finds it within the acceptable window.
3. No deployment warning banner appears on the page.

### Warning notice shown for moderately outdated deployment

1. The admin visits the overview page while the instance has not been re-deployed for more than two weeks but less than four weeks.
2. The notices partial detects the stale timestamp and renders a warning-level banner.
3. The banner informs the admin how long ago the last deployment occurred and recommends re-deploying from the main branch.
4. The banner also notes the increased risk of problems if the instance remains out of date.

### Danger notice shown for severely outdated deployment

1. The admin visits the overview page while the instance has not been re-deployed for more than four weeks.
2. The notices partial detects the highly stale timestamp and renders a danger-level banner.
3. The same advisory message is shown as in the warning case, but the banner uses the danger style to convey greater urgency.
