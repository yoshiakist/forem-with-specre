# @specre 01KJXS159QDWN1VEG2HY67NM54
module Api
  module V0
    class ReadinglistController < ApiController
      include Api::ReadinglistController

      before_action :authenticate!
    end
  end
end
