# @specre 01KJ75D28S88YETAPX6NF3ZP4C
module Emails
  class RemoveOldEmailsWorker
    include Sidekiq::Job

    sidekiq_options queue: :low_priority, retry: 10

    def perform
      EmailMessage.fast_destroy_old_retained_email_deliveries
    end
  end
end
