---
id: "01KJ1C3MFT988AX8WWC1G6EG0G"
name: "system_displays_social_media_profile_links"
status: "draft"
---

## Related Files

- `app/views/layouts/_social_media.html.erb` (Template)

## Functional Overview

The `_social_media.html.erb` partial renders a row of social media profile links as icon-only anchor elements in the main navigation sidebar. It iterates over all configured social media handles from `Settings::General.social_media_handles`, skipping any that are blank. For each present handle, it constructs the full profile URL via the `social_media_constructed_url` helper, which builds platform-specific URLs (e.g., `https://x.com/` for Twitter, `https://bsky.app/profile/` for Bluesky, the raw handle for Mastodon, and a generic `https://{platform}.com/` fallback for others). Each link opens in a new tab with `rel="noopener me"` and displays a platform icon via `crayons_icon_tag`. When more than five handles are configured, a compact layout is applied by omitting horizontal margins between icons.

## Key Members

- `compact_margin` — boolean flag set to `true` when more than 5 social media handles are configured; controls whether horizontal margin (`mx-1`) is applied to each icon link.
- `Settings::General.social_media_handles` — hash of platform keys (e.g., `twitter`, `github`, `mastodon`) to handle strings; blank handles are skipped.
- `social_media_constructed_url(social_media_type, handle)` — helper that returns a full profile URL; has explicit branches for `mastodon` (handle used as-is), `twitter` (`https://x.com/`), `bluesky` (`https://bsky.app/profile/`), `linkedin` (`https://www.linkedin.com/in/`), `youtube` (`https://www.youtube.com/@`), and a generic fallback.

## Scenarios

### Rendering multiple configured social media handles

1. The template reads `Settings::General.social_media_handles`, which contains a hash of platform names to handle strings.
2. It counts how many handles are non-blank to determine whether to use compact spacing.
3. For each platform with a non-blank handle, it generates an anchor tag pointing to the constructed profile URL.
4. Each anchor opens in a new tab and carries `rel="noopener me"` for security and identity linking.
5. The platform's icon is rendered inside the anchor using `crayons_icon_tag`, with the platform name capitalized as the accessible title.

### Applying compact layout when more than five handles are present

1. Before rendering any links, the template checks whether the count of non-blank handles exceeds 5.
2. If the count is greater than 5, `compact_margin` is set to `true` and the `mx-1` CSS class is omitted from each anchor element.
3. If the count is 5 or fewer, `compact_margin` is `false` and `mx-1` is applied, providing standard spacing between icons.

### Skipping blank handles

1. For each entry in `Settings::General.social_media_handles`, the template evaluates whether the handle value is blank.
2. If the handle is blank, the template skips that platform entirely using `next`.
3. No link or icon is emitted for unconfigured platforms.

### Constructing Mastodon URLs

1. When `social_media_type` is `mastodon`, the helper treats the stored handle as the full URL rather than a username slug.
2. The anchor `href` is set directly to the handle value without prepending any base domain.

## Failures / Exceptions

- If all configured social media handles are blank, the template produces no output (no anchor elements are rendered).
