# @specre 01KJ15Z6XANFFT1FA0YP2J2EQC
module Notifications
  class RemoveOldNotificationsWorker
    include Sidekiq::Job

    sidekiq_options queue: :low_priority, retry: 10

    def perform
      Notification.fast_destroy_old_notifications
    end
  end
end
