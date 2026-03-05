---
id: "01KHYYANBZBNB7XDZQA27N5P5Q"
name: "user_can_browse_subforems"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/subforems_controller.rb
- app/views/subforems/index.html.erb (Template)
- spec/requests/subforems_spec.rb (Test)

## Functional Overview

Any visitor (authenticated or not) can browse the public directory of subforems at `/subforems`. The page displays all discoverable, non-root subforems in a responsive grid layout. Each subforem card shows its name, community description, logo, and a follow button. Admins and subforem moderators see an additional edit link on each card. The page includes SEO meta tags (canonical URL, Open Graph, Twitter card).

## Scenarios

### User views the subforem directory

1. User navigates to `/subforems`
2. System queries all subforems where `discoverable` is true and `root` is false
3. System renders a responsive grid (4 columns on large screens, 2 on medium, 1 on small)
4. Each card displays the subforem's name (linked to the subforem), community description, logo image, and a follow button

### Admin sees edit controls

1. Admin or subforem moderator views the subforem directory
2. Each card includes an additional edit link that navigates to the subforem's edit page
3. Regular users and guests do not see the edit link

### Empty state

1. When no discoverable subforems exist, the page displays an empty state message
