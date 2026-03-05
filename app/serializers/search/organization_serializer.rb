# @specre 01KJ02HC7CPXANNH4W8KJWYC61
module Search
  class OrganizationSerializer < ApplicationSerializer
    attribute :class_name, -> { "Organization" }
    attributes :id, :name, :summary, :profile_image, :twitter_username, :slug
  end
end
