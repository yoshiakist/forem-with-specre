# @specre 01KJ0295AV619CEC61P9EVC0V8
# @specre 01KHYAKA53GF8RR3HJRFK3Y0A9
module Organizations
  class BustCacheWorker < BustCacheBaseWorker
    def perform(organization_id, slug)
      return unless organization_id && slug

      organization = Organization.find_by(id: organization_id)

      return unless organization

      EdgeCache::BustOrganization.call(organization, slug)
    end
  end
end
