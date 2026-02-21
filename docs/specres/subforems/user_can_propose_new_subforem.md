---
id: "01KHYYBET04W7WAZ1CNGMCEKAT"
name: "user_can_propose_new_subforem"
status: "draft"
---

## Related Files

- app/controllers/subforems_controller.rb
- app/views/subforems/new.html.erb (Template)

## Functional Overview

Authenticated users can visit a page to propose new subforems. The page explains that subforems are experimental community spaces for building intentional communities around shared interests. If a survey is configured, the page embeds a `SurveyTag` that allows users to submit their subforem proposal through the survey. If no survey is available, a warning message is displayed instead.

## Scenarios

### User views the proposal page with survey

1. User navigates to the new subforem page
2. System checks for a configured survey associated with subforem proposals
3. System renders an informational notice explaining that subforems are experimental
4. System embeds the survey via a `SurveyTag` liquid tag, allowing the user to submit their proposal

### User views the proposal page without survey

1. User navigates to the new subforem page when no survey is configured
2. System renders the informational notice
3. System displays a warning indicating that the proposal survey is not currently available
