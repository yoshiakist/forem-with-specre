# @specre 01KHZ6M3H0WPQNH4GKB6YPAR1T
module Users
  class HandleProfileSpamWorker
    include Sidekiq::Job

    def perform(user_id)
      user = User.find_by(id: user_id)
      return unless user

      Spam::Handler.handle_profile_update!(user: user)
    end
  end
end
