# @specre 01KJXS159QDWN1VEG2HY67NM54
module Api
  module V1
    class ReadinglistController < ApiController
      include Api::ReadinglistController

      before_action :authenticate_with_api_key!
    end
  end
end
