---
id: "01KHZ7FM5XC6DM0PAZZZ948707"
name: "user_can_follow_a_podcast"
status: "draft"
---

## Related Files

- `app/views/dashboards/following_podcasts.html.erb` (Template)
- `app/views/followings/podcasts.json.jbuilder` (Template)

## Functional Overview

A logged-in user can follow a podcast by clicking a "Follow" button rendered on the podcast episode index page or on an individual podcast episode show page. The button carries a `data-info` attribute populated by `DataInfo.to_json` containing the podcast's id and class name; client-side JavaScript in `followButtons.js` intercepts the click, updates the button UI optimistically, and POSTs to the `/follows` endpoint with `followable_type=Podcast`, `followable_id`, and a `verb` of either `unfollow` or `unfollow`'s inverse. The current user's list of followed podcasts is exposed via `FollowingsController#podcasts`, which queries `Follow` records of type `"Podcast"` and renders them in the dashboard's following-podcasts view (HTML) and via a JSON endpoint consumed by the API.

## Scenarios

### User follows a podcast from the episode index page

1. The user visits a podcast's episode listing page (e.g., `/some-podcast`).
2. The page renders a "Follow" button (`#user-follow-butt`) with `data-info` containing the podcast's id and class name (`Podcast`).
3. On page load, `followButtons.js` fetches the current follow status from `GET /follows/:id?followable_type=Podcast` and updates the button label to "Follow" or "Following" accordingly.
4. The user clicks the button.
5. The button UI updates optimistically (label changes to "Following", style changes to outlined).
6. A POST is sent to `/follows` with `followable_type=Podcast`, `followable_id`, and `verb=unfollow` (or `follow` when unfollowing is the intent, depending on current state).
7. If the server returns a non-200 response, an error modal is shown and the follow is considered failed.

### User follows a podcast from an episode show page

1. The user visits an individual podcast episode page (e.g., `/some-podcast/some-episode`).
2. A "Follow" button is rendered in the hero section of the page alongside the podcast title and artwork.
3. Follow button initialization and click handling proceed identically to the episode index page scenario above.

### Unauthenticated user attempts to follow a podcast

1. A logged-out user visits a podcast page containing a "Follow" button.
2. The user clicks the button.
3. `followButtons.js` detects the user is logged out (via `data-user-status` on `<body>`).
4. A login modal is shown instead of submitting a follow request.

### User views their followed podcasts on the dashboard

1. The authenticated user navigates to the dashboard's "Following Podcasts" section.
2. `FollowingsController#podcasts` queries the current user's `Follow` records of type `"Podcast"`, ordered by most recently followed, and paginates the result.
3. If any followed podcasts exist, the view renders a responsive card grid displaying each podcast's logo, name, and a link to its page.
4. If no podcasts are followed, a localized empty-state message is shown.

### API consumer fetches the list of followed podcasts

1. A client sends a request to the followings podcasts JSON endpoint.
2. The response is an array of objects each with `type_of: "podcast_following"`, the follow record id, and fields from the `api/v0/shared/follows` partial for the podcast.
