# @specre 01KJ6EB6TC32BW8DSXN5DVWY9M
class BillboardEventRollupWorker
  include Sidekiq::Worker

  sidekiq_options queue: :low_priority

  def perform
    month_ago = Date.current - 32.days
    BillboardEventRollup.rollup month_ago
  end
end
