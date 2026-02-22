# @specre 01KJ2SJQYZE780NB4SYY4CMW9G
module Credits
  class SyncCounterCache
    include Sidekiq::Job

    sidekiq_options queue: :low_priority, retry: 10

    def perform
      Credit.counter_culture_fix_counts only: %i[user organization]
    end
  end
end
