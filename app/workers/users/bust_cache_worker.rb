# @specre 01KHZ6KMGFYFBB8TCE6Q554D1Z
module Users
  class BustCacheWorker < BustCacheBaseWorker
    def perform(user_id)
      user = User.find_by(id: user_id)
      return unless user

      EdgeCache::BustUser.call(user)
    end
  end
end
