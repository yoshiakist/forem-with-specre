# @specre 01KHYAR0M26F2KE6CFGA3390RE
module Api
  module V0
    class OrganizationsController < ApiController
      include Api::OrganizationsController

      before_action :find_organization, only: %i[users listings articles]
    end
  end
end
