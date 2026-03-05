---
id: "01KJBK4DJHK81XKCTCTC53GGAE"
name: "system_validates_recaptcha_on_registration"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/re_captcha/check_enabled.rb`
- `app/services/re_captcha/check_registration_enabled.rb`
- `spec/services/re_captcha/check_enabled_spec.rb` (Test)
- `spec/services/re_captcha/check_registration_enabled_spec.rb` (Test)

## Functional Overview

The system determines whether reCAPTCHA should be shown to a user via two cooperating service objects. `ReCaptcha::CheckEnabled` evaluates whether reCAPTCHA is active for a given user by first confirming that the site key and secret key are both configured in `Settings::Authentication`, then applying a series of role- and activity-based rules: anonymous visitors always see the challenge, privileged users (tag moderators, trusted users, admins) are always exempt, suspended or spam-flagged users always see it, and regular authenticated users see it only if they have a vomit reaction against them or their account was created within the last month. `ReCaptcha::CheckRegistrationEnabled` builds on this by additionally requiring the `require_captcha_for_email_password_registration` setting to be enabled before presenting the challenge at the email/password registration form.

## Design Intent

The two-layer design separates general reCAPTCHA eligibility (`CheckEnabled`) from the registration-specific gate (`CheckRegistrationEnabled`). This allows `CheckEnabled` to be reused for other actions (e.g., abuse reports) while `CheckRegistrationEnabled` adds the extra admin-controlled toggle that is relevant only to the signup flow.

## Scenarios

### reCAPTCHA is disabled when keys are not configured

1. A visitor or any user attempts an action that would normally trigger reCAPTCHA.
2. The system detects that the reCAPTCHA site key or secret key is absent from authentication settings.
3. The system returns `false`; no reCAPTCHA challenge is presented regardless of the user's role or account age.

### reCAPTCHA is enabled for anonymous visitors

1. An unauthenticated visitor triggers a reCAPTCHA check.
2. The system confirms both keys are configured.
3. Because no user is provided, the system returns `true` and presents the challenge.

### reCAPTCHA is suppressed for privileged or established users

1. A logged-in user who is a tag moderator, trusted user, or admin triggers a reCAPTCHA check.
2. The system confirms keys are configured.
3. The system recognises the user's privileged role and returns `false`; no challenge is shown.
4. Likewise, an older regular user (account older than one month, no vomit reactions, not suspended) also receives `false`.

### reCAPTCHA is enforced for suspended, spam, vomited, or very new users

1. A logged-in user who is marked as suspended, spam, or has a confirmed vomit reaction against them triggers a reCAPTCHA check.
2. The system confirms keys are configured.
3. The system detects the high-risk indicators and returns `true`; a challenge is presented.
4. A newly created regular user (account within the last month) also triggers `true` by the recency rule.

### reCAPTCHA on the registration form requires an additional setting

1. A new visitor begins the email/password registration flow.
2. `ReCaptcha::CheckRegistrationEnabled` is called (no user argument).
3. The system first evaluates `ReCaptcha::CheckEnabled` without a user; if keys are not configured it returns `false` immediately.
4. If keys are configured, the system additionally checks the `require_captcha_for_email_password_registration` setting.
5. The challenge is shown only when both conditions are true; if either is false, registration proceeds without a reCAPTCHA challenge.

## Failures / Exceptions

- If either the reCAPTCHA site key or secret key is blank or nil, the entire check short-circuits to `false` regardless of all other conditions.
