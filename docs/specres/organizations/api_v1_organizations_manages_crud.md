---
id: "01KHYAR18XSDQE448P8GXMPR05"
name: "api_v1_organizations_manages_crud"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v1/organizations_controller.rb
- spec/requests/api/v1/organizations_spec.rb (Test)
- spec/requests/api/v1/docs/organizations_spec.rb (Test)

## Functional Overview

The Api::V1::OrganizationsController extends the shared API concern with full CRUD capabilities. It adds index, create, update, and destroy actions with role-based authentication (admin for update, super_admin for create/destroy) and supports flexible organization lookup by either ID or slug.

## Scenarios

### API v1 lists organizations with pagination

1. The caller requests a paginated list of organizations with optional page and per_page parameters.
2. The system returns selected index attributes: id, name, profile_image, slug, summary, tag_line, url.

### API v1 shows organization by ID or slug

1. The caller provides an id_or_slug parameter.
2. The system attempts lookup by id first, then by slug.
3. The system returns detailed profile attributes or raises RecordNotFound.

### API v1 creates organization (super_admin only)

1. The caller provides organization parameters including an optional profile_image (file or URL string).
2. If the profile_image is a URL string, the system converts it via `Images::SafeRemoteProfileImageUrl`.
3. The system authorizes via OrganizationPolicy, saves, and returns the created organization with 201 status.

### API v1 updates organization (admin only)

1. The caller provides updated attributes (name, profile_image, slug, summary, tag_line, url).
2. The system authorizes via InternalPolicy, updates, and returns the updated organization.
3. On validation failure, the system returns a 422 error with error messages.

### API v1 deletes organization (super_admin only)

1. The system authorizes and enqueues `Organizations::DeleteWorker` with `deleted_by_org_admin=false`.
2. The system returns a JSON message confirming deletion is scheduled.
