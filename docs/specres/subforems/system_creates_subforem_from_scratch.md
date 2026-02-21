---
id: "01KHYYH62ZG383CA1EG815V11C"
name: "system_creates_subforem_from_scratch"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/subforem.rb
- app/workers/subforems/create_from_scratch_worker.rb
- app/services/images/generate_subforem_images.rb
- spec/models/subforem_spec.rb (Test)
- spec/workers/subforems/create_from_scratch_worker_spec.rb (Test)
- spec/services/images/generate_subforem_images_spec.rb (Test)
- spec/factories/subforems.rb (Test)

## Functional Overview

When an admin provides a domain, brain dump, name, logo URL, and optional background image URL and locale, the `Subforem.create_from_scratch!` class method creates the subforem record and enqueues a `Subforems::CreateFromScratchWorker` Sidekiq job. The worker orchestrates the full automated setup: configuring community settings and locale, generating images (logo, favicon, social card) via `Images::GenerateSubforemImages`, and invoking AI services to generate community copy, tags, and an about page. The worker sets admin action timestamps at start and completion to track the setup lifecycle.

## Design Intent

The create-from-scratch workflow is asynchronous because image generation and AI calls are slow operations. By running in a background job, the admin gets immediate feedback (redirect to index) while the system completes setup. The worker is idempotent in its settings writes, so retries are safe.

## Scenarios

### System creates a subforem and enqueues setup

1. Admin provides domain, brain dump, name, logo URL, and optional background image and locale
2. `Subforem.create_from_scratch!` creates the database record with the domain
3. System enqueues `Subforems::CreateFromScratchWorker` with the subforem ID, brain dump, name, logo URL, background image URL, and locale

### Worker performs full automated setup

1. Worker sets `admin_action_taken_at` timestamp
2. Worker configures community name, default locale, and user experience settings (feed style, brand color)
3. Worker calls `Images::GenerateSubforemImages` which generates a resized logo (100x100), favicon, logo PNG (512x512), and a social media image (1000x500 composite)
4. Worker invokes AI services to generate community copy, suggested tags, and an about page (with locale support)
5. Worker sets `admin_action_completed_at` timestamp and logs success

### Image generation processes multiple formats

1. `Images::GenerateSubforemImages` downloads the logo image
2. Service generates resized logo, favicon, logo PNG, and social card versions using MiniMagick
3. If a background image is provided, it is used as the social card background; otherwise a template is used
4. Each generated image is uploaded via `ArticleImageUploader` and the URL is saved to settings

### Worker handles errors gracefully

1. If any step fails, the worker logs the error and notifies Honeybadger
2. The exception is re-raised so Sidekiq can retry (configured for 10 retries)
3. If the subforem doesn't exist, the worker raises an error immediately
