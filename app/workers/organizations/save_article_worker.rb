# @specre 01KJ02R9930HM3ZZNY5GTQB0X4
# @specre 01KHYAKARS8WVZ96MGFRRX02R5
module Organizations
  class SaveArticleWorker
    include Sidekiq::Job

    sidekiq_options queue: :high_priority

    def perform(article_id)
      Article.find(article_id).save
    end
  end
end
