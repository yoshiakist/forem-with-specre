# @specre 01KJ9R606N0EG98CQ1X82ECHHN
module Users
  class ResolveSpamReportsWorker
    include Sidekiq::Job

    sidekiq_options queue: :medium_priority, retry: 10, lock: :until_executing

    def perform(user_id)
      user = User.find_by(id: user_id)
      return unless user

      Users::ResolveSpamReports.call(user)
    end
  end
end
