---
id: "01KHZ7C4BEPF5TMJ68BXTZMMVP"
name: "author_can_embed_podcast_episode_in_article"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/liquid_tags/podcast_tag.rb`
- `app/assets/stylesheets/ltags/PodcastTag.scss`
- `app/views/podcast_episodes/_liquid.html.erb` (Template)
- `spec/liquid_tags/podcast_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a podcast episode into an article body by using the `{% podcast <url> %}` Liquid tag. The tag accepts a URL or path containing a podcast slug and episode slug, looks up the matching `Podcast` and `PodcastEpisode` records, validates that the episode belongs to the podcast, and renders an interactive player card showing the episode title, podcast title, podcast artwork, and play/pause controls. The rendered embed is styled responsively and initialises client-side playback via a JavaScript polling hook. Invalid or ambiguous links cause an error to be raised immediately at parse time so the article cannot be saved with a broken embed.

## Design Intent

Resolving the podcast and episode from slugs at render time (rather than storing IDs) keeps the Liquid tag input human-readable and URL-safe. Rejecting the tag at initialization rather than at render time surfaces errors to the author immediately, preventing broken embeds from reaching readers.

## Key Members

- `PARTIAL` — the Rails partial path (`podcast_episodes/liquid`) used to render the embed HTML
- `SCRIPT` — inline JavaScript that polls until `initializePodcastPlayback` is defined, then calls it to wire up the audio player
- `IMAGE_LINK` — a frozen hash mapping service names (`itunes`, `overcast`, `android`, `rss`) to their icon URLs, made available to the template for subscription links

## Scenarios

### Embedding a valid podcast episode

1. An author writes a `{% podcast <path> %}` tag in their article, where `<path>` contains a valid podcast slug and episode slug (e.g. `/my-podcast/episode-1`).
2. `PodcastTag` strips HTML, removes query strings, and splits the path to extract the last two segments as the podcast slug and episode slug.
3. The tag looks up the `Podcast` by slug and the `PodcastEpisode` by slug, then confirms the episode's `podcast_id` matches the podcast's `id`.
4. The tag renders the `podcast_episodes/liquid` partial, passing the resolved episode and podcast as locals.
5. The rendered HTML displays the episode title, podcast title, podcast artwork, and play/pause buttons styled by `.podcastliquidtag`.

### Initiating playback in the browser

1. The embed's inline script begins polling at 1 ms intervals for the global `initializePodcastPlayback` function to become available.
2. Once the function exists, the script calls `initializePodcastPlayback()` and clears the interval, wiring up the interactive audio player without requiring a page reload.

### Responsive display of the player card

1. On narrow viewports, the player card stacks vertically: artwork appears above the episode info panel.
2. On viewports 830 px wide or wider, the layout switches to a horizontal row with artwork on one side and episode info on the other.
3. While audio is playing, the `.playing` CSS class is added to the record element, causing the artwork to spin and swapping the play button for the pause button.

## Failures / Exceptions

- If the path has fewer than 2 or more than 5 slash-separated components, `PodcastTag` raises a `StandardError` with the i18n message `liquid_tags.podcast_tag.invalid_podcast_link`.
- If no `Podcast` record matches the podcast slug, or no `PodcastEpisode` record matches the episode slug, the same error is raised.
- If the found episode's `podcast_id` does not match the found podcast's `id` (i.e. the slug pair refers to records from different podcasts), the error is raised to prevent cross-podcast mismatches.
