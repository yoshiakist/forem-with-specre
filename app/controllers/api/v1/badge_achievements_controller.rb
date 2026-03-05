# @specre 01KJ6FJA4XS9P5A266ZFW6Q7Y4
module Api
  module V1
    class BadgeAchievementsController < ApiController
      include Api::BadgeAchievementsController

      before_action :authenticate!
      before_action :require_admin
    end
  end
end