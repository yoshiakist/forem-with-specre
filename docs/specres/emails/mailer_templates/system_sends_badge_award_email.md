---
id: "01KJ72KP1KB032AK6P3J2J6BFE"
name: "system_sends_badge_award_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/new_badge_email.html.erb`
- `app/views/mailers/notify_mailer/new_badge_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user earns a badge, the system sends a congratulatory email to that user. The email is delivered in both HTML and plain-text formats. It includes the badge title, badge image (HTML only), an optional default badge description, and an optional rewarding context message supplied by the rewarder. A profile link directs the recipient back to their own profile page. An unsubscribe token is embedded to allow the user to opt out of future badge notification emails.

## Design Intent

The rewarding context message is authored in Markdown and rendered to HTML for the HTML part of the email. Internal links within that message receive Ahoy click-tracking parameters appended directly to the path, while external links are routed through the `/ahoy/click` redirect endpoint. This keeps internal navigation lightweight (no extra redirect hop) while still tracking external click-outs. UTM parameters are intentionally omitted from internal links to avoid polluting first-party analytics.

## Key Members

- `badge_achievement` — the `BadgeAchievement` record being celebrated; carries the user, badge, and rewarding context
- `rewarding_context_message` — rendered HTML of the rewarder's Markdown message; may be nil or empty, in which case the block is omitted entirely
- `include_default_description` — boolean on `BadgeAchievement`; when true the badge's own description paragraph is shown
- `unsubscribe` — signed token scoped to `:email_badge_notifications`, embedded in the email footer for one-click unsubscription
- Subject line — resolved via `I18n.t("mailers.notify_mailer.new_badge")`, currently "You just got a badge"

## Scenarios

### Badge email sent to the recipient

1. A `BadgeAchievement` record is passed to the mailer as a parameter.
2. The system resolves the associated user and badge from the achievement record.
3. An unsubscribe token scoped to `:email_badge_notifications` is generated for the user.
4. The email is addressed to the user's email address with the subject "You just got a badge".
5. Both an HTML part and a plain-text part are rendered and delivered.

### HTML part — congratulation content

1. The user's name and the badge title appear in the greeting.
2. The badge image is displayed at 200 px height with an alt attribute set to the badge title.
3. If `include_default_description` is true, the badge's description paragraph is shown below the image.
4. If `rewarding_context_message` is present and non-empty, it is rendered as HTML inside an `<em>` block beneath the description.
5. A "Check out your profile" call-to-action button links to the user's profile URL.

### HTML part — internal link tracking

1. Any internal link (relative path) in the `rewarding_context_message` is decorated with `ahoy_click=true`, `t=`, `s=`, and `u=` query parameters directly on the original path.
2. No `/ahoy/click` redirect wrapper is applied to internal links.
3. No UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`) are added to internal links.

### HTML part — external link tracking

1. Any external link (absolute URL to a different domain) in the `rewarding_context_message` is rewritten to route through `/ahoy/click`.
2. The redirect carries `t=`, `s=`, and `u=` tracking parameters, with the original URL encoded as a query parameter.
3. The original external URL is not used directly as the `href`.

### HTML part — rewarding context message absent

1. If `rewarding_context_message` is nil or an empty string, the context message block is not rendered in the HTML part.

### Plain-text part

1. The congratulation line includes the user's name and the badge title.
2. If `include_default_description` is true, the badge description appears as plain text.
3. If `rewarding_context_message` is present and non-empty, it is stripped of HTML tags and rendered as plain text (links appear as anchor text only, with no URLs for inline links).
4. The user's full profile URL appears as a plain-text link.
5. If `rewarding_context_message` is nil or empty, it is omitted entirely from the text part.

## Failures / Exceptions

- If `rewarding_context_message` is nil or blank, both the HTML and text templates silently omit that section; no error is raised.
