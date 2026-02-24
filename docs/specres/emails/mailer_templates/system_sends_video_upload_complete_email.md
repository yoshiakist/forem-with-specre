---
id: "01KJ72K4BVPB3SWGWJ4TH12QS1"
name: "system_sends_video_upload_complete_email"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/mailers/notify_mailer.rb`
- `app/views/mailers/notify_mailer/video_upload_complete_email.html.erb`
- `app/views/mailers/notify_mailer/video_upload_complete_email.text.erb`
- `spec/mailers/notify_mailer_spec.rb` (Test)

## Functional Overview

When a video finishes processing, the system sends a transactional email to the article's author informing them that their video is ready. The email is addressed to the user associated with the article, carries the subject "Your video upload is complete", and provides a direct link to the article's edit page so the author can finalize and publish the video.

## Design Intent

Video processing is asynchronous and can take an indeterminate amount of time, so the author cannot simply wait on the page. A notification email closes the feedback loop, allowing the author to return to the editing workflow at the right moment without polling or guessing.

## Key Members

- `article` — the article whose video has finished processing; provides the edit URL and the owning user
- `user` — the article's author; determines the recipient email address and display name
- Subject line is sourced from the i18n key `mailers.notify_mailer.video_upload` ("Your video upload is complete")

## Scenarios

### Video processing completes and notification email is dispatched

1. A background job finishes processing the video for a given article and invokes the `video_upload_complete_email` mailer action with that article as a parameter.
2. The system resolves the article's author from `article.user` and sets that user as the sole recipient (`to: user.email`).
3. The system sets the subject to "Your video upload is complete".
4. The HTML body greets the user by name and presents a prominent link to the article's edit page so they can finalize and publish the video.
5. The plain-text body confirms the video is processed and includes the same edit-page URL as a bare link.
6. The email is enqueued for delivery.

## Failures / Exceptions

- If the article has no associated user, `article.user` will be nil and address resolution will fail; the caller is responsible for ensuring the article has a persisted user before invoking the mailer.
