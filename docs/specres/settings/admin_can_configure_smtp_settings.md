---
id: "01KHZ41WMS2556S431RYZG2Q1X"
name: "admin_can_configure_smtp_settings"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings/smtp_settings_controller.rb`
- `app/models/settings/smtp.rb`
- `app/lib/constants/settings/smtp.rb`
- `app/views/admin/settings/forms/_smtp.html.erb` (Template)
- `spec/models/settings/smtp_spec.rb` (Test)
- `spec/system/admin/config/admin_updates_smtp_settings_spec.rb` (Test)

## Functional Overview

A super-admin can configure the outbound email transport by setting up a custom SMTP server. The `Settings::SMTP` model stores address, port, domain, authentication method, credentials, from-address, and reply-to address. When minimum settings (address, username, password) are provided, the system uses the custom SMTP configuration; otherwise it falls back to SendGrid settings. The admin form conditionally shows a checkbox to toggle own email server when SendGrid is enabled, and reveals the full SMTP configuration form when the toggle is active.

## Scenarios

### Admin configures custom SMTP server

1. Admin enters SMTP `address`, `port` (default: 25), `domain`, `user_name`, and `password`
2. Admin selects `authentication` method from: plain, login, or cram_md5
3. Admin sets `from_email_address` and `reply_to_email_address` (validated as email format)
4. System persists the configuration; `provided_minimum_settings?` returns true
5. The `settings` method returns the custom provider configuration hash for use by Action Mailer

### System falls back to SendGrid when SMTP is unconfigured

1. Admin has not provided minimum SMTP settings (address, username, and password)
2. `provided_minimum_settings?` returns false
3. The `settings` method returns `fallback_sendgrid_settings` for email delivery

### Admin toggles own email server with SendGrid enabled

1. When SendGrid is enabled and SMTP is not yet configured, the form shows a checkbox labeled "Use your own email server"
2. Checking the box reveals the full SMTP configuration form
3. When SendGrid is enabled and SMTP is already configured, both the checkbox and the form are visible
4. When SendGrid is disabled, the SMTP form is shown directly without the checkbox
