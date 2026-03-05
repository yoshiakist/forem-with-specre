---
id: "01KHZ6GG5GD766PRZK1SE50KMG"
name: "system_processes_profile_images"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/uploaders/profile_image_uploader.rb`
- `app/services/images/profile.rb`
- `app/services/images/profile_image_generator.rb`
- `app/services/images/safe_remote_profile_image_url.rb`
- `spec/uploaders/profile_image_uploader_spec.rb` (Test)
- `spec/services/images/profile_spec.rb` (Test)
- `spec/services/images/profile_image_generator_spec.rb` (Test)
- `spec/services/images/safe_remote_profile_image_url_spec.rb` (Test)

## Functional Overview

The system handles all aspects of profile image processing through four cooperating components. `ProfileImageUploader` manages file uploads via CarrierWave, enforcing an 8 MB size limit, an allowlist of image extensions, and a secure randomised filename. `Images::Profile` provides an optimisation entry point that resizes images to a square crop at a requested pixel length and falls back to a hosted backup image when none is available. `Images::ProfileImageGenerator` generates a random default image by selecting one of 40 bundled asset images when no remote URL can be used. `Images::SafeRemoteProfileImageUrl` sanitises incoming remote URLs by rejecting nil, blank, and non-HTTP strings, upgrading plain HTTP to HTTPS, or falling back to `ProfileImageGenerator` when the URL is unusable.

## Design Intent

The backup and fallback layering is deliberate: `Images::Profile` supplies a remote CDN backup for the optimisation pipeline, while `SafeRemoteProfileImageUrl` supplies a locally generated file for contexts where a remote URL is required but absent. This separation keeps the upload pipeline independent of the optimisation pipeline and avoids coupling URL sanitisation to CDN availability.

## Key Members

- `ProfileImageUploader::MAX_FILE_SIZE` — upper bound of 8 MB enforced during upload
- `Images::Profile::BACKUP_LINK` — CDN URL used when a user's image URL is nil
- `Images::Profile.for(attribute)` — factory that mixes a size-aware accessor into any class that stores an image URL attribute

## Scenarios

### Uploading a profile image

1. A user submits an image file for their profile.
2. `ProfileImageUploader` checks that the file size is within 1 byte to 8 MB and that the file extension is in the allowed list (jpg, jpeg, jpe, gif, png, ico, bmp, dng, webp).
3. If the file passes validation, the uploader generates a UUID-based secure token and stores the file under `uploads/<model>/<mount>/<id>/` with a filename combining the token and the original extension.
4. EXIF and GPS metadata are stripped from the stored image.

### Rejecting an unsupported or oversized file

1. A user submits a file with an extension outside the allowlist (e.g., pdf) or exceeding 8 MB.
2. `ProfileImageUploader` raises a `CarrierWave::IntegrityError`, and the file is not stored.

### Optimising a profile image for display at a given size

1. A caller requests a profile image URL at a specific pixel length (default 120).
2. `Images::Profile.call` passes the image URL (or `BACKUP_LINK` if the URL is nil) to `Optimizer.call` with equal width and height and a crop mode of `"crop"`.
3. The optimizer returns a resized, cropped image URL suitable for rendering at the requested size.

### Mixing image URL access into a model class

1. A class includes `Images::Profile.for(:image_url)`.
2. The mixin adds an `image_url_for(length:)` method to the class.
3. Calling that method delegates to `Images::Profile.call` with the instance's image URL and the provided length.

### Sanitising a remote profile image URL

1. The system receives a candidate URL for a remote profile image.
2. `Images::SafeRemoteProfileImageUrl.call` checks whether the URL starts with `"http"`.
3. If yes, any `http://` prefix is upgraded to `https://` and the URL is returned.
4. If the URL is nil, blank, or does not start with `"http"`, the system calls `Images::ProfileImageGenerator.call`, which opens a randomly selected bundled PNG asset and returns the file handle.

## Failures / Exceptions

- Uploading a file with a disallowed extension raises `CarrierWave::IntegrityError`.
- A nil or blank profile image URL passed to `Images::Profile.call` results in the `BACKUP_LINK` being sent to the optimizer rather than an error being raised.
- A nil, blank, or non-HTTP URL passed to `Images::SafeRemoteProfileImageUrl.call` silently falls back to a randomly generated local image file instead of surfacing an error.
