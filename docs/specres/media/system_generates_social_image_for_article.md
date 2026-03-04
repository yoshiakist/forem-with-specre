---
id: "01KJVEZN3YK9PYFVQ7FW9BBN7M"
name: "system_generates_social_image_for_article"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/images/generate_social_image_magickally.rb`
- `app/workers/images/social_image_worker.rb`
- `app/helpers/social_image_helper.rb`
- `app/lib/html_css_to_image.rb`
- `spec/services/images/generate_social_image_magickally_spec.rb` (Test)
- `spec/lib/html_css_to_image_spec.rb` (Test)

## Functional Overview

When an article (or a user or organization) is given a social image, the system composes a branded PNG by layering a template background, a colored stripe, the subforem logo, the author's profile photo with a rounded mask, and the article title, publication date, and author name as text. The image is then uploaded via `ArticleImageUploader` and the resulting URL is saved to the article's `social_image` column. Image generation is dispatched asynchronously via `Images::SocialImageWorker` (a Sidekiq job). An alternative HTML/CSS-based path is provided through `HtmlCssToImage`, which posts HTML and CSS to the external hcti.io API and caches the returned URL for six weeks to avoid redundant generation costs.

## Design Intent

MiniMagick operations modify image objects in place, so fresh image objects must be opened for every article processed. Logo URLs and author image URLs are cached on the generator instance across articles within a single job run to avoid redundant external lookups when many articles share the same subforem or author. Pure black (`#000000`) is remapped to near-black (`#111212`) because MiniMagick renders a pure-black fill as transparent, producing an invisible stripe.

## Key Members

- `@cached_subforem_id` / `@cached_logo_url` — instance-level cache so the subforem logo URL is only fetched when the subforem changes between articles
- `@cached_user_id` / `@cached_author_image_url` — instance-level cache so the author image URL is only recalculated when the user changes
- `HtmlCssToImage::CACHE_EXPIRATION` — 6 weeks; controls how long the hcti.io image URL is stored in Rails cache

## Scenarios

### Generating a social image for a single article

1. `Images::SocialImageWorker` receives an article ID and class name, looks up the record, and calls `Images::GenerateSocialImageMagickally.call(article)`.
2. The service reads the article's subforem to look up the correct logo URL and reads the author's profile image URL, caching both on the instance.
3. Fresh MiniMagick image objects are created for the template background, logo, author photo, and rounded mask.
4. A colored stripe is drawn across the top of the background using the author's brand color (pure black is shifted to `#111212`).
5. The logo (if present) is outlined in white, resized to 64x64, and composited onto the upper right of the background.
6. The article title (truncated to 128 characters and word-wrapped based on length) is drawn in bold at a dynamically scaled font size; author name and publication date are drawn in the lower left.
7. The author's profile photo is composited at 64x64 in the lower left with a rounded-corner mask applied on top.
8. The composed image is written to a tempfile, uploaded via `ArticleImageUploader`, and the tempfile is deleted.
9. The returned URL is saved to `article.social_image` and the article's edge cache is busted.

### Generating social images in bulk for a user

1. `GenerateSocialImageMagickally.call(user)` iterates over all of the user's published articles that have no organization and no main image.
2. For each article, files are read and the image is generated using the user's brand color and name.
3. Each article's `social_image` column is updated with the resulting URL. The subforem logo and author image URL caches are reused across articles to minimize external calls.

### Generating social images in bulk for an organization

1. `GenerateSocialImageMagickally.call(organization)` iterates over all of the organization's published articles that have no main image.
2. The organization's name and background color hex are used in place of a user's details.
3. Each article's `social_image` column is updated; caching applies as in the user case.

### Generating an image via the HTML/CSS-to-image API

1. Caller invokes `HtmlCssToImage.fetch_url(html:, css:, google_fonts:)`.
2. The method derives a cache key from the inputs and returns the cached URL immediately if one exists.
3. On a cache miss, it POSTs to hcti.io with HTTP Basic Auth using configured API credentials.
4. On success the URL is written to the Rails cache with a 6-week expiration; on failure the platform's main social image is returned as a fallback without caching.

## Failures / Exceptions

- Any `StandardError` raised during MiniMagick image generation is caught, logged via `Rails.logger.error`, and reported to Honeybadger; the job does not re-raise.
- If `HCTI_API_USER_ID` or `HCTI_API_KEY` is blank, `HtmlCssToImage.url` skips the external call and returns the fallback image immediately.
- If the hcti.io API returns an error response (e.g., rate-limit exceeded), the fallback image is returned and the result is not cached.
- If the author's profile image URL does not start with `http`, the backup profile image URL (`Images::Profile::BACKUP_LINK`) is used instead.
- If no logo URL is configured for a subforem, no logo image is opened or composited.
