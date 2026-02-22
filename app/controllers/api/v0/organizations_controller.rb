# @specre 01KHZGVB146XQBKF66V2THG07T
module Api
  module V0
    class OrganizationsController < ApiController
      include Api::OrganizationsController

      before_action :find_organization, only: %i[users listings articles]
    end
  end
end
