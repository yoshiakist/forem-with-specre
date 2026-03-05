---
id: "01KJCKBBKHXER1P381MJEJF8P0"
name: "reader_shares_article_via_social_or_link_copy"
status: "draft"
---

## Related Files

- `app/views/articles/_actions.html.erb`
- `app/views/articles/_fullscreen_embed.html.erb`
- `app/javascript/packs/articlePage.jsx`
- `app/javascript/packs/webShare.js`
- `spec/requests/articles/articles_show_spec.rb` (Test)

## Functional Overview

On the article show page, a reader can share the article through multiple channels via a dropdown triggered by a share button in the article actions bar. The dropdown presents social media links for Twitter, LinkedIn, Facebook, and Mastodon (desktop only), a "Copy link" button that writes the article URL to the clipboard and announces success via an ARIA live region, and a Web Share API entry point for supported mobile browsers. On native Android, the share button bypasses the dropdown and calls `AndroidBridge.shareText` directly. The fullscreen embed mode replicates the same share UI inside a modal dialog opened by the "More Options" button, with its own copy-button handler that uses `navigator.clipboard.writeText` directly. A "Report Abuse" link is also grouped inside the same dropdown.

## Scenarios

### Reader clicks a social media share link

1. The reader opens the article show page and clicks the share button (overflow icon) in the actions bar.
2. The share dropdown opens, revealing social links for Twitter, LinkedIn, Facebook, and Mastodon (visible on desktop only via `.Desktop-only`).
3. The reader clicks a social link; it opens in a new tab with the article URL, title, description, and (for Twitter) the author's handle and community hashtag pre-filled in the share intent URL.
4. The dropdown closes automatically once the link is clicked.

### Reader copies the article link to clipboard

1. The reader opens the share dropdown and clicks the "Copy link" button (`#copy-post-url-button`).
2. `copyArticleLink` reads the article URL from the button's `data-postUrl` attribute and calls `copyToClipboard` (Clipboard API with runtime fallback).
3. On success, `showAnnouncer` unhides the `#article-copy-link-announcer` element, providing a polite ARIA live-region announcement that the link was copied.
4. When the dropdown is later closed, `hideCopyLinkAnnouncerIfVisible` hides the announcer again to reset state.

### Reader shares via Web Share API on mobile

1. On a mobile browser that supports the Web Share API, the `<web-share-wrapper>` custom element renders a share link inside the dropdown using the `web-share-button` template.
2. The reader taps the share link; the custom element invokes `navigator.share` with the article URL, title, and description.
3. The native OS share sheet appears, allowing the reader to share through any installed app.

### Reader shares from fullscreen embed mode

1. When an article is rendered in fullscreen embed mode (`data-type-of="fullscreen_embed"`), the actions sidebar still renders `_actions.html.erb` via a partial.
2. The "More Options" button (`#article-show-more-button`) is intercepted by `initializeFullscreenEmbed`; clicking it opens the universal modal with the share/extra-menu content from `#extra-menu-content` instead of the standard dropdown.
3. Inside the modal, a dedicated copy-button handler uses `navigator.clipboard.writeText` directly and auto-hides the success announcer after 3 seconds.
4. Social links and the Web Share API entry point are available in the modal the same way as in the standard dropdown.

## Design Intent

Social links are restricted to `.Desktop-only` because mobile devices have the Web Share API and native share sheets as a superior mechanism. The `<web-share-wrapper>` custom element is rendered unconditionally in markup but only produces a visible link when the browser supports `navigator.share`, keeping the progressive-enhancement pattern self-contained in the custom element. The ARIA live region on the copy-link announcer provides accessible feedback without requiring a focus change. The fullscreen embed modal approach is necessary because the standard dropdown would be clipped or z-index-conflicted inside the fixed fullscreen layout.

## Failures / Exceptions

- If the Clipboard API is unavailable (non-secure context or unsupported browser), `copyToClipboard` falls back to a legacy execCommand approach; if that also fails the announcer is never shown and the copy silently fails.
- If `navigator.clipboard.writeText` fails in the fullscreen embed modal copy handler, the error is unhandled and the success announcer is not shown.
- On native Android (`isNativeAndroid('shareText')`), the dropdown is never initialized; the share button directly calls `AndroidBridge.shareText(location.href)` instead.
