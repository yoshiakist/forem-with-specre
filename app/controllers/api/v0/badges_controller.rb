# @specre 01KJ6FFA2FH0HVDCGYH9XQB3GG
module Api
  module V0
    class BadgesController < ApiController
      include Api::BadgesController

      before_action :authenticate_with_api_key_or_current_user!
      before_action :require_admin
      skip_before_action :verify_authenticity_token
    end
  end
end