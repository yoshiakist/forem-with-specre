---
id: "01KJ72SS278ECC5FW24CY96BHP"
name: "system_delivers_data_export_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/export_email.html.erb`
- `app/views/mailers/notify_mailer/export_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a user's data export has been completed, the system sends a notification email to the user's address that includes the exported archive as an attachment. The email carries a subject line indicating the export is ready, and the attached ZIP file is named using the current date in ISO 8601 format (e.g., `devto-export-2026-02-24.zip`). Both an HTML and a plain-text version of the email body are rendered, each telling the user to check the attached file.

## Design Intent

Delivering the export as an email attachment keeps the download self-contained and avoids requiring the user to return to the site. Dating the filename makes it easy for recipients to identify the archive later and distinguishes multiple exports over time.

## Key Members

- `attachment` — the binary content of the generated ZIP archive, supplied via mailer params
- `export_filename` — computed from the current date as `devto-export-<YYYY-MM-DD>.zip`
- `email` — recipient address, supplied via mailer params
- Subject — localised via `I18n.t("mailers.notify_mailer.export")`; resolves to a string indicating the export is ready

## Scenarios

### Sending the export email

1. The caller invokes `NotifyMailer` with `email` (recipient address) and `attachment` (ZIP binary) as params.
2. The mailer computes today's date in ISO 8601 format and constructs the filename `devto-export-<date>.zip`.
3. The ZIP binary is attached to the email under that filename with content type `application/zip`.
4. The mailer addresses the email to the supplied recipient and sets the subject to the localised export-ready string.
5. The email is delivered with both an HTML body ("Your content has been exported. Please check the attached file.") and an equivalent plain-text body.
6. The recipient receives the email and can download the ZIP attachment directly from their mail client.

## Failures / Exceptions

- If `attachment` or `email` is missing from params, the mailer will raise an error before the message is built; callers are responsible for ensuring both values are present.
