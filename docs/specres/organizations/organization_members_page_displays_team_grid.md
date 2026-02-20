---
id: "01KHYAZ2T9RHPJ445FZC71BW0G"
name: "organization_members_page_displays_team_grid"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/views/organizations/members.html.erb

## Functional Overview

The organization members page renders a responsive grid of all organization members, displaying each member's profile image, name, username, and a follow button. The page title includes the organization name and total member count.

## Scenarios

### Members page renders team grid

1. The page title is set to the organization name.
2. A heading displays the organization name with the total member count in parentheses.
3. Each member is rendered as a card in a responsive grid layout (1 to 4 columns depending on viewport).
4. Each member card displays a profile image linked to the member's profile page, with lazy loading.
5. Each member card includes a follow button with the member's data info for JavaScript interaction.
6. Each member card shows the member's display name and @username, both linked to the member's profile.
