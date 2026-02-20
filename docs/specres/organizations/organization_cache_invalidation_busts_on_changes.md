---
id: "01KHYAKA53GF8RR3HJRFK3Y0A9"
name: "organization_cache_invalidation_busts_on_changes"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_organization.rb
- app/workers/organizations/bust_cache_worker.rb
- spec/services/edge_cache/bust_organization_spec.rb (Test)
- spec/workers/organizations/bust_cache_worker_spec.rb (Test)

## Functional Overview

The organization cache invalidation system consists of an EdgeCache::BustOrganization service that purges the organization's profile page and all associated article pages from the edge cache, and a BustCacheWorker that triggers this service asynchronously after organization changes.

## Scenarios

### Service busts organization and article caches

1. The service receives an organization and slug.
2. If either is nil, the service returns immediately.
3. The service busts the cache for the organization's profile path (`/<slug>`).
4. The service iterates over all organization articles and busts the cache for each article's path.
5. If an error occurs while iterating articles, the service logs the error and continues.

### Worker triggers cache busting asynchronously

1. The worker receives organization_id and slug.
2. If either parameter is nil, the worker exits silently.
3. The worker looks up the organization by ID; exits silently if not found.
4. The worker calls `EdgeCache::BustOrganization` with the organization and slug.
