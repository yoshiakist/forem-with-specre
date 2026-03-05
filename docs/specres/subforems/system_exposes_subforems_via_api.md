---
id: "01KHYYJCP2TRNXM24G12C072KD"
name: "system_exposes_subforems_via_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/subforems_controller.rb
- app/controllers/api/v1/subforems_controller.rb
- app/controllers/concerns/api/subforems_controller.rb
- app/views/api/v0/subforems/index.json.jbuilder
- app/views/api/v1/subforems/index.json.jbuilder
- spec/requests/api/v0/subforems_spec.rb (Test)
- spec/requests/api/v1/subforems_spec.rb (Test)

## Functional Overview

The public API exposes a listing of subforems via `GET /api/subforems` across both v0 and v1 versions. The shared logic lives in the `Api::SubforemsController` concern, which queries all discoverable or root subforems ordered by score descending. Each subforem is serialized to JSON with id, domain, root flag, name, description, logo image URL, and cover image URL. Responses include surrogate-key caching headers and a 5-minute public cache with stale-while-revalidate and stale-if-error directives.

## Scenarios

### Client lists discoverable subforems

1. Client sends `GET /api/subforems` (v0 or v1)
2. System queries subforems where `discoverable` is true or `root` is true, ordered by score descending
3. System serializes each subforem via Jbuilder with fields: `id`, `domain`, `root`, `name`, `description`, `logo_image_url`, `cover_image_url`
4. System returns JSON array with appropriate caching headers

### API sets caching headers

1. Response includes a `Surrogate-Key` header derived from the subforem record keys
2. Response includes `Cache-Control: public, max-age=300` (5 minutes)
3. Response includes `stale-while-revalidate=300` and `stale-if-error=86400` directives

### V1 API supports version header

1. Client sends the request with the v1 Accept header
2. System routes to the v1 controller which inherits the same shared behavior from the concern
