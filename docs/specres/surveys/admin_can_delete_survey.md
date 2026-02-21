---
id: "01KHZMJ17G1A41XF5RZPAVH91P"
name: "admin_can_delete_survey"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/surveys_controller.rb`
- `spec/requests/admin/surveys_spec.rb` (Test)

## Functional Overview

A super-admin can permanently delete a survey via the admin panel. When the destroy action is triggered, the system locates the survey by its ID and calls destroy on it, which cascades to remove associated polls and poll options. After the attempt — whether successful or not — the admin is redirected to the surveys index page. On success, a success flash message is shown; on failure, a danger flash message is shown containing the model's validation errors.

## Design Intent

Both the success and failure paths redirect to the surveys index rather than re-rendering a detail page. This means the destroy action does not leave the admin on a broken or stale resource page if deletion fails. The cascade deletion of associated polls and poll options is handled by the model's `destroy` call rather than manual iteration, relying on ActiveRecord associations to clean up dependent records.

## Scenarios

### Successful deletion

1. Admin submits a DELETE request for an existing survey.
2. The system finds the survey and calls destroy, which removes the survey and all associated polls and poll options.
3. A success flash message ("Survey has been deleted!") is set.
4. Admin is redirected to the admin surveys index page.

### Deletion failure

1. Admin submits a DELETE request for an existing survey.
2. The system finds the survey and calls destroy, but destruction fails (e.g., a model callback returns false or raises an error).
3. A danger flash message containing the survey's error messages is set.
4. Admin is redirected to the admin surveys index page.

## Failures / Exceptions

- If `@survey.destroy` returns false (destruction blocked by a callback), the admin is redirected to the index with a danger flash showing the error details rather than being shown a separate error page.
