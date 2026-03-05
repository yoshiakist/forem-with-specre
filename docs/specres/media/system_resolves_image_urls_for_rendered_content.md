---
id: "01KJ1C23JZY0T5QCNX103SR5MM"
name: "system_resolves_image_urls_for_rendered_content"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/models/media_store.rb`
- `app/services/articles/enrich_image_attributes.rb`
- `app/services/content_renderer.rb`
- `app/lib/redcarpet/render/html_rouge.rb`
- `spec/models/media_store_spec.rb` (Test)
- `spec/factories/media_stores.rb` (Test)
- `spec/services/markdown_processor/parser_spec.rb` (Test)
- `app/workers/articles/enrich_image_attributes_worker.rb`
- `spec/workers/articles/enrich_image_attributes_worker_spec.rb` (Test)
- `spec/services/articles/enrich_image_attributes_spec.rb` (Test)

## Functional Overview

When article or comment content is rendered, the system replaces external image URLs with internally stored, CDN-backed output URLs. A `MediaStore` record maps each original URL to an output URL, which is automatically populated via `ArticleImageUploader` on first save. During Markdown rendering, `Redcarpet::Render::HTMLRouge` intercepts every image and absolute-URL link containing an image, looks up the original URL in `MediaStore`, and substitutes the stored output URL if one exists. A separate enrichment pass (`Articles::EnrichImageAttributes`) runs after HTML is produced to set `width`, `height`, and `data-animated` attributes on `<img>` tags by fetching image dimensions using FastImage, and also updates `main_image_height` on the article. When the `store_images` feature flag is active and AWS is configured, `ContentRenderer` can pre-populate `MediaStore` records synchronously before the Markdown-to-HTML conversion begins, ensuring the renderer finds stored URLs immediately.

## Design Intent

Storing images in a `MediaStore` table decouples the original external URL from the final served URL, allowing transparent CDN or bucket migration without touching article bodies. The lookup at render time (rather than write time) means that newly stored URLs are picked up on the next render without requiring a content re-save. Enriching image dimensions in a separate post-processing pass avoids blocking the rendering pipeline and can be run asynchronously.

## Key Members

- `MediaStore#original_url` — the source URL used as the lookup key
- `MediaStore#output_url` — the internally stored or CDN URL substituted during rendering; auto-populated by `ArticleImageUploader` via `before_validation` if absent
- `MediaStore#media_type` — enum (`image`, `video`, `audio`) classifying the stored media
- `Articles::EnrichImageAttributes::IMAGES_IN_LIQUID_TAGS_SELECTORS` — CSS selectors identifying images inside Liquid tag wrappers that are excluded from dimension enrichment

## Scenarios

### Image URL substitution during Markdown rendering

1. Content containing a Markdown image (`![alt](https://example.com/image.jpg)`) or an HTML `<img>` within a Markdown link is passed to `MarkdownProcessor::Parser` for rendering.
2. `Redcarpet::Render::HTMLRouge#image` is called for each image token. If the `src` is an absolute HTTP/HTTPS URL, it queries `MediaStore` by `original_url`.
3. If a matching record exists, the rendered `<img>` tag uses `output_url`; otherwise the original URL is used unchanged.
4. For Markdown links whose content is an `<img>` tag, `HTMLRouge#link` parses the content, extracts the image source, delegates to `#image` for URL resolution, and wraps the resolved image in an `<a>` tag.

### MediaStore record creation and output URL assignment

1. A new `MediaStore` is created (via `first_or_create`) with an `original_url` and no `output_url`.
2. The `before_validation` callback `set_output_url_if_needed` fires; because `output_url` is blank, it instantiates `ArticleImageUploader` and calls `upload_from_url` with the original URL.
3. The uploader returns the internally stored URL, which is assigned to `output_url` and persisted.
4. Subsequent lookups by `original_url` return the already-set `output_url` without re-uploading.

### Synchronous image pre-storage before rendering

1. `ContentRenderer#process` is called with `synchronous_detail_detection: true` when the `store_images` feature flag is enabled and an AWS bucket is configured.
2. The renderer scans the raw Markdown for image URLs via regex patterns for both Markdown syntax and HTML `<img>` tags.
3. URLs already pointing to the configured S3 bucket are excluded; remaining unique URLs are each looked up or created in `MediaStore` via `first_or_create`.
4. Markdown is then processed by `MarkdownProcessor::Parser`, which will find the pre-created `MediaStore` records during the rendering step above.

### Article image attribute enrichment after HTML generation

1. After an article's processed HTML is generated, `Articles::EnrichImageAttributes.call` is invoked with the article.
2. If an AWS bucket is configured, `store_image_if_appropriate` first scans the article's raw Markdown for image URLs and creates `MediaStore` records for any not yet stored.
3. The processed HTML is parsed with Nokogiri; images inside Liquid tag containers are excluded from enrichment.
4. For each remaining `<img>`, if the `src` is a relative path the corresponding file is retrieved from the uploader store; absolute URLs are used directly.
5. FastImage fetches the image dimensions (with a 10-second timeout); `width` and `height` attributes are set, and `data-animated="true"` is added for GIFs.
6. The article's `main_image_height` is computed: hardcoded to 500 for YouTube thumbnails, proportionally calculated for the `limit` cover image fit mode, or taken from the community setting; the updated HTML and height are persisted.

## Failures / Exceptions

- If `ArticleImageUploader#upload_from_url` fails or returns blank during `MediaStore` validation, `output_url` remains unset and the record may not reflect a valid stored URL.
- In `store_image_if_appropriate`, individual URL storage failures are rescued and logged as errors without aborting the overall enrichment process.
- If FastImage times out or cannot determine dimensions, `width` and `height` attributes are not set; the fallback `main_image_height` is 300 when cover image fit is `limit`, or the configured `cover_image_height` otherwise.
- If a relative image `src` refers to a file not present in the uploader store, the image is skipped during enrichment (the file existence check returns early).
- Any `StandardError` raised during the top-level `store_image_if_appropriate` call is rescued and logged, preventing enrichment errors from surfacing to callers.
- `ContentRenderer#process` and `ContentRenderer#process_article` wrap all processing in a rescue block that re-raises as `ContentParsingError`.
