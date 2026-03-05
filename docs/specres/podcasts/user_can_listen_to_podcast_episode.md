---
id: "01KHZ78WJ7S3X0KQ8EVH6RD0DE"
name: "user_can_listen_to_podcast_episode"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/javascript/utilities/podcastPlayback.js`
- `app/assets/stylesheets/podcast-episodes-show.scss`
- `app/views/podcast_episodes/show.html.erb` (Template)
- `app/views/podcast_episodes/_podcast_bar.html.erb` (Template)
- `spec/requests/podcasts/podcast_episodes_show_spec.rb` (Test)
- `spec/system/podcasts/user_visits_podcast_episode_spec.rb` (Test)

## Functional Overview

When a user visits a podcast episode page, they see a hero section with a spinning vinyl record image that doubles as the play/pause button. Clicking the record loads the episode audio into a persistent bottom bar and begins playback. The bar exposes controls for play/pause, mute/unmute, volume, playback speed, and scrubbing. Playback state (current time, volume, playing status) is persisted in `localStorage` under the key `media_playback_state_v3` so that navigation away and back resumes from the same position. On iOS and Android, audio is delegated to native handlers via `window.Forem.Runtime.podcastMessage`; on web, a standard HTML `<audio>` element is used. Analytics events are fired to Ahoy on play and pause actions.

## Design Intent

Playback state is stored in `localStorage` rather than server-side so that resumption works without a network round-trip and without requiring the user to be signed in. The native bridging strategy (sending messages to `window.ForemMobile`) lets the same JavaScript code path serve both web and mobile app contexts, with the runtime detection (`initRuntime`) selecting the appropriate backend at startup.

## Key Members

- `media_playback_state_v3` — `localStorage` key holding a JSON object with `currentTime`, `duration`, `playing`, `muted`, `volume`, `playbackName`, and `html` fields
- `window.activeEpisode` — slug of the episode currently loaded in the player
- `window.activePodcast` — slug of the podcast currently loaded in the player
- `window.Forem.audioInitialized` — boolean guard preventing double-initialization across page navigation
- `window.Forem.Runtime.podcastMessage` — function set at runtime to either native bridge or `undefined` (web)

## Scenarios

### User plays an episode for the first time

1. User visits a podcast episode page at `/<podcast_slug>/<episode_slug>`.
2. The page renders the hero with a spinning record image, the episode title, and an optional publication date.
3. `initializePodcastPlayback` runs: it detects the platform, reads or creates audio state from `localStorage`, and attaches click handlers to the record button.
4. User clicks the record button; the audio HTML is injected into the podcast bar and `loadAudio` begins buffering.
5. Playback starts, the record image gains the `playing` class and begins spinning, and the bottom bar becomes visible with a progress indicator.
6. An Ahoy `Podcast Player Streaming` event is tracked with `action: play`.

### User pauses and resumes playback

1. While the episode is playing, the user clicks the record button or the bar's play/pause control.
2. `playPause` detects that `currentAudioState().playing` is `true` and calls `pauseAudioPlayback`.
3. The `playing` class is removed from the record and bar controls, and the Ahoy event is tracked with `action: pause`.
4. Current time and state are saved to `localStorage`.
5. User clicks again; `playAudio` seeks to the saved `currentTime` and resumes, re-applying the `playing` class.

### User adjusts volume or mutes audio

1. User clicks the volume icon or the mute button in the podcast bar.
2. `muteUnmute` toggles the `muted` flag in `localStorage` state and swaps the visibility of the mute/volume icons.
3. On web, `audio.muted` is set directly; on native, a `podcastMessage` with `action: muted` is dispatched.
4. User drags the volume slider; `updateVolume` updates `audio.volume` (or dispatches `action: volume`) and saves state.

### User scrubs to a different position

1. User clicks anywhere on the progress bar in the podcast bar.
2. `goToTime` calculates the target time as a percentage of total duration based on the click's horizontal position.
3. On web, `audio.currentTime` is updated directly; on native, a `podcastMessage` with `action: seek` is dispatched.
4. The progress bar and time display update to reflect the new position.

### Episode is not playable over HTTPS

1. User visits an episode page where `@episode.https?` is `false`.
2. The show template renders an unplayable warning message (`views.podcasts.statuses.unplayable`) instead of a functional record button.
3. A "Click here to download" link pointing to `@episode.media_url` is shown as an alternative.

## Failures / Exceptions

- If `localStorage` contains corrupt JSON, `currentAudioState` catches the parse error and falls back to `newAudioState`, initializing a clean state.
- If `playAudio` rejects (e.g., browser autoplay policy), playback is retried once after a 5 ms delay, and `spinPodcastRecord('initializing...')` shows a status message on the record button.
- If the episode page is visited from a non-mobile browser, `isNativeIOS` and `isNativeAndroid` both return `false` and the standard web `<audio>` element is used.
- If `sendMetadataMessage` fails to parse the episode metadata JSON, the error is logged to the console and native metadata is not sent, but playback continues.
