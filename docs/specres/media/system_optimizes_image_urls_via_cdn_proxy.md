---
id: "01KJVEZHZX5TZ7F9VR43E8WYFS"
name: "system_optimizes_image_urls_via_cdn_proxy"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/images/optimizer.rb`
- `app/view_objects/cloud_cover_url.rb`
- `spec/services/images/optimizer_spec.rb` (Test)
- `spec/view_objects/cloud_cover_url_spec.rb` (Test)

## Functional Overview

The system rewrites external image URLs through a CDN proxy service to deliver optimized, resized images. `Images::Optimizer` selects among three backends — imgproxy, Cloudinary, and Cloudflare Images — in priority order based on which credentials are configured, routing each image URL through the chosen backend with caller-supplied dimensions and crop mode. `CloudCoverUrl` is a thin view-object layer on top of `Images::Optimizer` that resolves cover-image dimensions and crop settings from per-subforem configuration, strips legacy Cloudinary prefix nesting from already-proxied URLs, and applies a fixed YouTube thumbnail override before handing off to the optimizer.

## Design Intent

The priority order (imgproxy > Cloudinary > Cloudflare) lets operators migrate between CDN providers by toggling credentials alone. Cloudflare can also be promoted over Cloudinary for S3-hosted images via a feature flag (`cloudflare_preferred_for_hosted_images`), enabling gradual traffic migration without a code change. Relative URLs and blank inputs are short-circuited immediately so that local assets are never rewritten.

## Key Members

- `DEFAULT_CL_OPTIONS` — baseline Cloudinary transformation options (fetch type, progressive flag, auto quality/format, signed URL); callers may override individual keys
- `DEFAULT_IMGPROXY_OPTIONS` — baseline imgproxy options including a 500 KB max-bytes cap, smart gravity, and auto-rotate
- `CLOUDFLARE_DIRECTORY` — directory segment in the Cloudflare URL template; defaults to `"cdn-cgi"` and can be overridden via `ApplicationConfig["CLOUDFLARE_IMAGES_DIRECTORY"]`
- `crop` parameter — accepted as `"crop"` (fill/cover semantics) or anything else (limit/scale-down/fit semantics); translated per-backend

## Scenarios

### CDN backend selection

1. The caller invokes `Images::Optimizer.call` with an external image URL and optional width, height, and crop.
2. If the URL is blank or starts with `/`, the original value is returned unchanged.
3. If imgproxy is configured (key and salt present), the URL is processed through imgproxy and returned.
4. If imgproxy is absent but Cloudinary credentials are present and Cloudflare is not contextually preferred, the URL is processed through Cloudinary.
5. If Cloudflare is the only configured backend (or is contextually preferred over Cloudinary), the URL is processed through Cloudflare Images.
6. If no backend is configured, the original URL is returned unchanged.

### Cloudflare contextual preference for hosted images

1. When Cloudflare Images is enabled and the feature flag `cloudflare_preferred_for_hosted_images` is active, the system checks whether the image originates from the configured S3 bucket or is already a Cloudflare-proxied URL.
2. If the image is S3-hosted or already proxied through Cloudflare, the system bypasses Cloudinary even when Cloudinary credentials are present and routes through Cloudflare instead.
3. Non-hosted images continue to use the default priority order.

### Cover image URL optimization via CloudCoverUrl

1. A view requests an optimized cover image URL by instantiating `CloudCoverUrl` with a raw URL and an optional subforem ID.
2. In development environments the raw URL is returned as-is; in other environments processing continues.
3. The system looks up the subforem's configured cover image height and crop fit from `Settings::UserExperience`; width is fixed at 1000 px.
4. If the URL contains `ytimg.com`, height is overridden to 500 px and crop is forced to `"crop"` regardless of configuration.
5. If the URL is already a Cloudinary-proxied URL containing a `w_1000/` prefix segment, the nesting is unwrapped to retrieve the original source URL.
6. The resolved source URL and dimensions are passed to `Images::Optimizer.call`, and the resulting CDN-proxied URL is returned.

### Crop mode translation across backends

1. A caller specifies `crop: "crop"` to request fill/cover-style cropping that exactly fills the target dimensions.
2. `Images::Optimizer` translates `"crop"` to backend-specific terminology: `"fill"` for Cloudinary (or `"imagga_scale"` when the legacy `CROP_WITH_IMAGGA_SCALE` flag is set and `never_imagga` is not passed), `"cover"` for Cloudflare, and `resizing_type: "fill"` for imgproxy.
3. Any crop value other than `"crop"` triggers scale-down semantics: `"limit"` for Cloudinary, `"scale-down"` for Cloudflare, and `resizing_type: "fit"` for imgproxy.

### Nested Cloudflare URL unwrapping

1. When building a Cloudflare URL, if the source image URL is itself a Cloudflare-proxied URL (starts with the known Cloudflare prefix), the system extracts the inner original URL by parsing the path for an embedded `http(s)://…` segment.
2. The unwrapped original URL is used as the `src` in the new Cloudflare template, preventing double-nesting of proxy parameters.

## Failures / Exceptions

- Blank or nil input to `Images::Optimizer.call` is returned as nil/blank without raising.
- Blank or nil input to `CloudCoverUrl#call` returns nil immediately.
- If a Cloudflare-nested URL contains no recognizable embedded URL in its path, the extraction returns nil and the resulting Cloudflare URL is built with an empty src segment rather than raising.
- GIF images processed through Cloudinary receive a reduced quality value of 66 instead of `"auto"` to cap file size.
