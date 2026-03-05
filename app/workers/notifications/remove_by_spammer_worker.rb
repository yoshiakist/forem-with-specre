# @specre 01KJ15Z6XANFFT1FA0YP2J2EQC
module Notifications
  class RemoveBySpammerWorker
    include Sidekiq::Job

    sidekiq_options queue: :low_priority, retry: 10

    def perform(user_id)
      user = User.find_by(id: user_id)
      return unless user

      Notifications::RemoveBySpammer.call(user)
    end
  end
end
