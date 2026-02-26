---
id: "01KJBWT5HAQGGSECGZJ20D6PCX"
name: "author_can_create_article_with_video"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/videos_controller.rb`
- `app/controllers/video_states_controller.rb`
- `app/services/article_with_video_creation_service.rb`
- `app/policies/video_policy.rb`
- `app/views/videos/new.html.erb` (Template)
- `app/views/mailers/notify_mailer/video_upload_complete_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/video_upload_complete_email.text.erb` (Template)
- `spec/services/article_with_video_creation_service_spec.rb` (Test)
- `spec/requests/videos_spec.rb` (Test)
- `spec/requests/video_states_update_spec.rb` (Test)
- `spec/policies/video_policy_spec.rb` (Test)

## Functional Overview

An author who meets eligibility requirements can upload a video file directly to S3 and create a draft article associated with that video. The upload form (`/videos/new`) is gated by `VideoPolicy`, which requires the feature flag `enable_video_upload` to be on and the user to be in good standing and to have had their account for at least two weeks (or to be an admin when post creation is admin-restricted). On form submission, `ArticleWithVideoCreationService` creates a draft article with the video URL, sets its state to `PROGRESSING`, and derives the video code, HLS source URL, and thumbnail URL from the S3 key. Once AWS Elastic Transcoder finishes encoding, it calls back `VideoStatesController#create` with a signed key; the controller verifies the key, marks the article's `video_state` as `COMPLETED`, and triggers a notification email to the author.

## Design Intent

The AWS callback endpoint (`/video_states`) skips CSRF verification and Pundit authorization deliberately: it is called by AWS, not by a browser session. Authentication is instead performed by comparing a shared secret (`video_encoder_key`) stored in site settings, keeping the surface area of the unauthenticated route minimal.

## Key Members

- `video_state` — enum-like string on `Article`; starts as `"PROGRESSING"` when the upload begins and transitions to `"COMPLETED"` on AWS callback.
- `video_code` — the S3 key fragment extracted from the upload URL; used as the lookup key when AWS sends the completion webhook.
- `VIDEO_SERVICE_URL` — CloudFront CDN base URL from which HLS playlist and thumbnail URLs are constructed.

## Scenarios

### Author accesses the upload form

1. A signed-in user with an account older than two weeks navigates to `/videos/new`.
2. The system checks `VideoPolicy#new?`: the feature flag is enabled and the user is in good standing with a sufficiently old account.
3. The system renders the S3 direct-upload form, allowing the user to select a video file.

### Author submits a video upload

1. The author selects a video file; the form posts the resulting S3 URL to `POST /videos`.
2. The system authorizes the request via `VideoPolicy#create?` (same eligibility rules as above).
3. `ArticleWithVideoCreationService` creates a draft article with `video_state: "PROGRESSING"`, sets the video code extracted from the S3 key, and derives the CloudFront HLS URL and thumbnail URL.
4. The author is redirected to the new article's edit page.

### AWS signals encoding completion

1. AWS Elastic Transcoder sends a `POST /video_states?key=<encoder_key>` request with a JSON payload containing the video's S3 input key.
2. The controller verifies the `key` query parameter against the configured `video_encoder_key`; if it does not match, the request is rejected with `422 Unprocessable Entity`.
3. The system looks up the article by its `video_code`; if not found, it responds with `404 Not Found`.
4. On a match, the article's `video_state` is updated to `"COMPLETED"` and a notification email is sent to the author.

## Failures / Exceptions

- `VideoPolicy` raises `UserSuspendedError` if the user's account is suspended, and `UserRequiredError` if no user is signed in.
- Accounts created within the last two weeks are denied access (policy returns `false`) unless the user is an admin and post creation is restricted to admins.
- When `enable_video_upload` is `false`, `VideoPolicy#create?` returns `false` immediately, blocking all video creation regardless of account age.
- An invalid or missing AWS encoder key causes `VideoStatesController` to return `422 Unprocessable Entity` without updating any data.
- If the AWS payload references a `video_code` that does not match any article, the controller returns `404 Not Found`.
