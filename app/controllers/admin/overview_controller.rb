# @specre 01KJ6QD968CHB6HNK748HR81KV
# @specre 01KJ7FK7N2EJG4M5C7JYHGZGJ0
module Admin
  class OverviewController < Admin::ApplicationController
    layout "admin"
    def index
    end

    def stats
      period = (params[:period] || 7).to_i
      period = [7, 30, 90].include?(period) ? period : 7
      
      stats = Admin::StatsData.new(period).call
      
      render json: stats
    end
  end
end