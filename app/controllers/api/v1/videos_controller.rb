# @specre 01KJBWV962FQYVV8TD7XMHWN5Q
module Api
  module V1
    class VideosController < ApiController
      include Api::VideosController

      before_action :set_cache_control_headers, only: %i[index]
    end
  end
end
