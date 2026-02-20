# @specre 01KHY987S3SNX2YV4C0ZHSHEK3
module GithubRepos
  class UpdateLatestWorker
    include Sidekiq::Job

    sidekiq_options queue: :medium_priority, retry: 10

    def perform
      GithubRepo.update_to_latest
    end
  end
end
