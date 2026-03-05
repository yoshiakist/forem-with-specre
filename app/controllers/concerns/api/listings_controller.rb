# @specre 01KJXWGTKXY2KHWQQ23XG2PNZF
# @specre 01KJXWGP0V021QH50BJW9Q1KKD
# @specre 01KJXWC077QF4CMYHXFFQ278TR
# @specre 01KJXWBCMHBTSTY8EW25W3B4CV
# @specre 01KJXWBM12SRTZ3BCRGK8G10YT
module Api
  module ListingsController
    extend ActiveSupport::Concern
    include Pundit::Authorization


    def index
      render json: []
    end

    def show
      render json: {}
    end

    def create
      head :ok
    end

    def update
      head :ok
    end

    def destroy
      head :ok
    end

    private
    attr_accessor :user
    alias current_user user
  end
end