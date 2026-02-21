---
id: "01KHYYC8DH90XT7E7QYRPVDT2W"
name: "user_can_select_subforem_when_creating_post"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/assets/javascripts/subforemSelectionModal.js
- app/views/shared/_subforem_selection_modal.html.erb (Template)
- spec/requests/subforem_selection_modal_spec.rb (Test)

## Functional Overview

When a user is on the root subforem and initiates post creation, a full-screen modal presents all postable subforems so the user can choose which community to post to. Each option displays the subforem's logo, name, and description. Clicking an option navigates the user to that subforem's new post page. The modal is controlled by vanilla JavaScript and can be closed via the close button, backdrop click, or the Escape key.

## Scenarios

### User sees the selection modal on root subforem

1. User is browsing the root subforem
2. User clicks the "Create Post" button, which triggers `window.openSubforemModal()`
3. System displays a full-screen modal listing all postable subforems from `Subforem.cached_postable_array`
4. Each option shows the subforem's logo, community name, and description

### User selects a subforem and is redirected

1. User clicks on a subforem option in the modal
2. System navigates the user to the selected subforem's new post page

### User dismisses the modal

1. User can close the modal by clicking the close button, clicking the backdrop, or pressing the Escape key
2. The modal is hidden and body scroll is restored

### Modal is not shown on non-root subforems

1. When the user is already on a non-root subforem, the selection modal is not rendered in the page
