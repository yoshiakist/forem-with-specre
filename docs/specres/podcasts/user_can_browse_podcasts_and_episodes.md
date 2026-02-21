---
id: "01KHZ78Z9A3R2NWZF2B6EZ82AJ"
name: "user_can_browse_podcasts_and_episodes"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/podcast_episodes_controller.rb`
- `app/decorators/podcast_episode_decorator.rb`
- `app/javascript/podcasts/PodcastEpisode.jsx`
- `app/javascript/podcasts/PodcastFeed.jsx`
- `app/javascript/podcasts/TodaysPodcasts.jsx`
- `app/javascript/podcasts/index.js`
- `app/javascript/articles/PodcastArticle.jsx`
- `app/views/podcast_episodes/index.html.erb` (Template)
- `app/views/podcast_episodes/_episodes_feed.html.erb` (Template)
- `app/views/podcast_episodes/_meta.html.erb` (Template)
- `spec/requests/podcasts/podcast_episodes_index_spec.rb` (Test)
- `spec/decorators/podcast_episode_decorator_spec.rb` (Test)
- `spec/views/podcast_episodes/index.html.erb_spec.rb` (Test)
- `spec/system/podcasts/user_visits_podcasts_root_page_spec.rb` (Test)
- `app/javascript/podcasts/__tests__/PodcastEpisode.test.jsx` (Test)
- `app/javascript/podcasts/__tests__/TodaysPodcasts.test.jsx` (Test)

## Functional Overview

When a user navigates to `/pod`, the system renders a public podcast index page that displays up to six of the most recently published available episodes, a section of up to four featured podcast shows, and a full browsable list of all available podcasts. Only episodes and podcasts that are both published and reachable are shown. Each episode card links directly to the episode page and shows the episode title, podcast name, cover image, and a human-readable publication date. The `PodcastEpisodeDecorator` enriches raw episode records with formatted date strings and mobile-player metadata. Frontend Preact components (`PodcastEpisode`, `TodaysPodcasts`, `PodcastFeed`) render episode cards in sidebar and feed contexts. The controller sets surrogate-key cache headers on the index response to support CDN purging.

## Design Intent

The controller is entirely public (no authorization), reflecting that podcast browsing is an unauthenticated experience. Surrogate keys are scoped to each episode record so that CDN caches can be purged at episode granularity without invalidating the whole index. The decorator pattern isolates presentation logic (date formatting, mobile metadata) from the ActiveRecord model, keeping the model clean and the view layer thin.

## Key Members

- `@podcast_episodes` — decorated collection of the 6 most recent available episodes, ordered by `published_at` descending
- `@featured_podcasts` — up to 4 featured, available podcasts, ordered alphabetically by title
- `@more_podcasts` — all available podcasts for the browse section, ordered alphabetically
- `readable_publish_date` — returns a short, locale-formatted date; omits year when the episode was published in the current year
- `published_timestamp` — returns the publication date as a UTC ISO 8601 string for machine-readable `datetime` attributes
- `mobile_player_metadata` — hash of `podcastName`, `episodeName`, and `podcastImageUrl` used by native mobile clients

## Scenarios

### Browsing the podcast index page

1. User visits `/pod` without authentication.
2. The system queries for the 6 most recently published available episodes and up to 4 featured podcasts.
3. The page renders a grid of episode cards, each showing the episode cover image, title, podcast name, and publication date.
4. If featured podcasts exist, a "Featured Shows" section is displayed below the recent episodes.
5. A full "Browse" section lists all available podcasts with their logos and titles.

### Viewing only reachable and published content

1. User visits `/pod`.
2. Episodes marked as unreachable or belonging to unpublished podcasts are excluded from all sections.
3. Only episodes and podcasts whose `available` scope conditions are satisfied appear in the rendered page.

### Navigating to a podcast or episode

1. User clicks on an episode card image or title link.
2. The browser navigates to `/<podcast_slug>/<episode_slug>`.
3. User clicks a podcast logo or title in the Browse section.
4. The browser navigates to `/<podcast_slug>`.

### Displaying episode publication dates

1. An episode with a `published_at` value in the current year is displayed with a short date format (e.g., "Jan 5").
2. An episode published in a prior year is displayed with a short format that includes the two-digit year (e.g., "Jan 5 '23").
3. An episode without a `published_at` value displays no date.
4. A machine-readable `<time datetime="...">` element is always emitted alongside a `time-ago-indicator-initial-placeholder` span for progressive enhancement.

### Inline sidebar feed (TodaysPodcasts / PodcastFeed)

1. A sidebar or feed area renders a `TodaysPodcasts` wrapper with a "Today's Podcasts" heading linking to `/pod`.
2. Each episode inside the wrapper is rendered as a `PodcastEpisode` card showing the podcast cover image, podcast name, and episode title.
3. Each card links to the episode at `/<podcast_slug>/<episode_slug>`.

## Failures / Exceptions

- When `params[:q]` is present (search context), surrogate-key headers are not set, preventing unintended CDN caching of search results.
- When no featured podcasts exist, the "Featured Shows" section is omitted entirely from the rendered page.
- When an episode has no `image_url`, the podcast's own image is used as the fallback cover image.
