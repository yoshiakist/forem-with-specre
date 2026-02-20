# @specre 01KHYCJNHZ6V29EK1MP1PGSCT6
module Api
  module V1
    class TagsController < ApiController
      include Api::TagsController

      before_action :set_cache_control_headers, only: %i[index]
    end
  end
end
