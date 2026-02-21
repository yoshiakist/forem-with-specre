---
id: "01KHZ7BNHPQDAKZA5SBMDTGM65"
name: "admin_can_manage_podcasts"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/podcasts_controller.rb`
- `app/models/podcast_episode_appearance.rb`
- `app/views/admin/podcasts/index.html.erb` (Template)
- `app/views/admin/podcasts/edit.html.erb` (Template)
- `spec/requests/admin/podcasts_spec.rb` (Test)
- `spec/models/podcast_episode_appearance_spec.rb` (Test)

## Functional Overview

Super-admin users can view, search, and manage podcasts through the admin panel. The index page lists all podcasts with their episode counts, reachability, publication status, and owners, and supports title-based search with pagination. From the edit page, admins can update podcast metadata (title, feed URL, description, platform URLs, images, slug, and flags like `reachable`, `featured`, and `published`), assign new owners by user ID, and trigger asynchronous episode fetching via `Podcasts::GetEpisodesWorker`. The `PodcastEpisodeAppearance` model enforces that each user can appear on a given episode only once and that the role must be either `host` or `guest`.

## Key Members

- `PODCAST_ALLOWED_PARAMS` — whitelist of permitted podcast attributes for mass-assignment: `title`, `feed_url`, `description`, `itunes_url`, `overcast_url`, `android_url`, `soundcloud_url`, `website_url`, `twitter_username`, `pattern_image`, `main_color_hex`, `slug`, `image`, `featured`, `reachable`, `published`
- `PodcastEpisodeAppearance#role` — enum-like string field; valid values are `host` and `guest`

## Scenarios

### Listing podcasts

1. An authenticated super-admin navigates to `GET /admin/content_manager/podcasts`.
2. The system queries all podcasts with a left outer join on episodes, annotates each with an episode count, orders by creation date descending, and paginates at 50 per page.
3. The index view renders a table showing each podcast's ID, title, feed URL, episode count, reachability, publication status, status notice, and owners.

### Searching podcasts by title

1. An admin submits the search form on the index page with a title query string.
2. The system filters the paginated podcast list to those whose title matches the query (case-insensitive substring match).
3. Only matching podcasts appear in the table.

### Updating podcast attributes

1. An admin opens a podcast's edit page and modifies one or more fields (e.g., title, feed URL, description, platform URLs, slug, images, or boolean flags).
2. The admin submits the form via `PUT /admin/content_manager/podcasts/:id`.
3. If the update succeeds, the system redirects to the index page with a success notice.
4. If validation fails, the edit form is re-rendered with error messages.

### Adding a podcast owner

1. On the edit page, an admin enters a user ID and submits the "Add Owner" form via `POST /admin/content_manager/podcasts/:id/add_owner`.
2. If the user ID resolves to a valid user, a `PodcastOwnership` record is created and the admin is redirected to the index with a success notice.
3. If the user ID does not correspond to an existing user, the admin is redirected back to the edit page with an error message.

### Fetching podcast episodes

1. On the edit page, an admin optionally sets a fetch limit and/or checks the "Force" option, then submits via `POST /admin/content_manager/podcasts/:id/fetch_podcasts`.
2. The system enqueues `Podcasts::GetEpisodesWorker` with the podcast ID, the specified limit (or `nil` for all recent episodes), and the force-update flag.
3. The admin is redirected to the index page with a notice confirming the fetch was scheduled.

## Failures / Exceptions

- Adding an owner with a non-existent user ID redirects back to the edit page with an error notice; no `PodcastOwnership` record is created.
- A `PodcastEpisodeAppearance` with an invalid role (anything other than `host` or `guest`) or a duplicate `podcast_episode_id`/`user_id` pair fails validation and is not saved.
