# @specre 01KJ6FJA4XS9P5A266ZFW6Q7Y4
module Api
  module V0
    class BadgeAchievementsController < ApiController
      include Api::BadgeAchievementsController

      before_action :authenticate_with_api_key_or_current_user!
      before_action :require_admin
      skip_before_action :verify_authenticity_token
    end
  end
end