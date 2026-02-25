# @specre 01KJ9MTBJ0F7WTG0KSNXPGF3N9
module Api
  module V1
    class UsersController < ApiController
      include Api::UsersController

      before_action :authenticate_with_api_key!, only: %i[me search suspend unpublish]
    end
  end
end
