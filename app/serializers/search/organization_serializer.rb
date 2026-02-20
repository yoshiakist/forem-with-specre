# @specre 01KHYAG7500GXRZGY07Y91X18W
module Search
  class OrganizationSerializer < ApplicationSerializer
    attribute :class_name, -> { "Organization" }
    attributes :id, :name, :summary, :profile_image, :twitter_username, :slug
  end
end
