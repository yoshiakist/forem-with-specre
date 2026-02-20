---
id: "01KHY99D5ZW1JPV9A0GAQGK90W"
name: "github_repos_frontend_displays_repos"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/javascript/githubRepos/githubRepos.jsx
- app/javascript/githubRepos/singleRepo.jsx
- app/javascript/packs/githubRepos.jsx
- app/javascript/githubRepos/__tests__/githubRepos.test.jsx (Test)
- app/javascript/githubRepos/__tests__/singleRepo.test.jsx (Test)

## Functional Overview

The GitHub Repos frontend is a Preact-based UI that allows users to view their GitHub repositories and toggle which ones are featured on their Forem profile. The `GithubRepos` component fetches the repository list from the `/github_repos` endpoint, while `SingleRepo` renders each row with a select/remove button. The pack entry point mounts the component into a `#github-repos-container` element and re-initializes on InstantClick page transitions.

## Scenarios

### Loading state displays while fetching repositories

1. On mount, the component renders a loading indicator with the title "Loading GitHub repositories".
2. It initiates a GET request to `/github_repos` to fetch the user's repositories.

### Successful fetch renders the repository list

1. When the fetch returns a successful response, the component renders a list of `SingleRepo` components.
2. Each `SingleRepo` receives the repo's `github_id_code`, `name`, `fork` status, and `featured` status as props.

### Error state displays an alert

1. If the fetch fails or returns a non-OK response, the component renders an error alert with the error message.
2. The error is reported to Honeybadger.

### SingleRepo displays repo name with fork indicator

1. Each repo row displays the repository name.
2. Forked repositories display a "fork" indicator badge.
3. Non-forked repositories do not display the fork indicator.

### SingleRepo toggles featured status

1. A non-featured repo displays a "Select" button.
2. A featured repo displays a "Remove" button and applies the `github-repo-row-featured` CSS class.
3. Clicking the button sends a POST to `/github_repos/update_or_create` with the `github_id_code` and the toggled `featured` value.
4. The button is disabled during the request and re-enabled on response.
5. The component updates its local state with the `featured` value from the server response.

### Pack initializes on page load and InstantClick transitions

1. The pack renders `GithubRepos` into the DOM element with ID `github-repos-container`.
2. On InstantClick `change` events, the component is re-rendered to support turbolinks-style navigation.
