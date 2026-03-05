---
id: "01KJ1C8DKS21XYDGCTHY01V45T"
name: "author_can_add_cover_video_to_article"
status: "draft"
---

## Related Files

- `app/javascript/article-form/components/CoverVideoLink.jsx`
- `app/javascript/article-form/utilities/videoParser.js`

## Functional Overview

When composing an article, an author can attach a cover video by entering a URL from a supported platform — YouTube, Mux, or Twitch. A button in the article form opens a modal dialog where the author types or pastes the URL. The modal validates the URL against patterns for each supported provider and either saves the value or displays an inline error. The utility module (`videoParser.js`) provides two exported functions used elsewhere in the form: `parseVideoUrl`, which normalises a raw URL into a typed embed descriptor (`{ embedUrl, type, videoId }`), and `getVideoThumbnail`, which derives a static thumbnail URL for YouTube and Mux videos.

## Design Intent

The modal is kept as an isolated inner component (`VideoLinkModal`) that is not exported, keeping the public API surface to a single `CoverVideoLink` component. Validation inside the modal uses simple regex patterns rather than full URL parsing, while the utility module uses the native `URL` constructor for robust parsing — this split avoids pulling the heavier parser into the modal render path. Twitch embeds require a `parent` domain parameter for security; the parser reads `window.location.hostname` at parse time so the value is always current.

## Key Members

- `videoSourceUrl: string` — the currently saved video URL passed into `CoverVideoLink`; controls button label and pre-populates the modal
- `onVideoUrlChange: func` — callback invoked with the new URL string (or `null` when the video is removed)
- `parseVideoUrl(url)` returns `{ embedUrl, type, videoId }` where `type` is `'youtube'`, `'mux'`, or `'twitch'`
- `getVideoThumbnail(videoInfo)` returns a thumbnail URL string for YouTube and Mux; returns `null` for Twitch

## Scenarios

### Author opens the modal for the first time

1. The article form renders a `CoverVideoLink` button labelled "Cover Video Link" because no video has been saved yet.
2. The author clicks the button; the `VideoLinkModal` opens with an empty URL field and a summary of supported formats.
3. The author dismisses the modal by clicking Cancel; the modal closes and no change is propagated.

### Author saves a valid video URL

1. The author opens the modal and enters a valid YouTube, Mux, or Twitch URL into the text field.
2. The author submits the form; the modal validates the URL against provider-specific patterns and finds a match.
3. `onSave` is called with the trimmed URL, which propagates to `onVideoUrlChange`; the modal closes.
4. The button label changes to "Change Video Link", reflecting that a video is now attached.

### Author submits an unsupported URL

1. The author types a URL that does not match YouTube, Mux, or Twitch patterns.
2. On submit, validation fails and an inline error message is displayed: "Please enter a valid YouTube, Mux, or Twitch video URL."
3. The modal remains open; no value is saved.

### Author removes the current video

1. The modal opens pre-populated with the existing URL; the button reads "Update Link" and a "Remove" button is visible.
2. The author clicks "Remove"; `onSave` is called with an empty string, which `CoverVideoLink` converts to `null` before passing to `onVideoUrlChange`.
3. The modal closes and the button reverts to "Cover Video Link".

### Consumer parses a video URL to embed and thumbnail

1. A consumer calls `parseVideoUrl` with a raw URL string.
2. The function attempts parsing as YouTube, then Mux, then Twitch in order.
3. On the first successful match it returns `{ embedUrl, type, videoId }`; if no provider matches it returns `null`.
4. A consumer may then call `getVideoThumbnail` with the result to obtain a static thumbnail URL for YouTube or Mux; Twitch returns `null` because no public thumbnail API is used.

## Failures / Exceptions

- Submitting a blank URL is treated as a removal: `onSave('')` is called and the modal closes without an error.
- Any URL that fails provider-pattern matching shows the inline error and blocks submission.
- `parseVideoUrl` and the individual parser functions silently return `null` for malformed URLs that cause the `URL` constructor to throw; errors are caught internally.
- `parseTwitchUrl` returns `null` for Twitch channel stream URLs (`twitch.tv/<channel>`); only `twitch.tv/videos/<id>` paths are accepted.
