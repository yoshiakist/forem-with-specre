# @specre 01KJ9MTBJ0F7WTG0KSNXPGF3N9
module Api
  module V0
    class UsersController < ApiController
      include Api::UsersController

      before_action :authenticate!, only: %i[me]
    end
  end
end
