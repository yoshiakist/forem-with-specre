# @specre 01KJV8A14A58JBDS2RRK1MY5YH
module Moderator
  class SinkArticles
    def self.call(user_id)
      Moderator::SinkArticlesWorker.perform_async(user_id)
    end
  end
end
