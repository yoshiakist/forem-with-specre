# @specre 01KJ1SBPYYJH4XJS6P8SW1HSG2
module GithubRepos
  class UpdateLatestWorker
    include Sidekiq::Job

    sidekiq_options queue: :medium_priority, retry: 10

    def perform
      GithubRepo.update_to_latest
    end
  end
end
