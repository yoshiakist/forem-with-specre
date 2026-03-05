# @specre 01KHZ7FNBPTBWCMXWYERHJHSS0
module EdgeCache
  class BustPodcast
    def self.call(path)
      return unless path

      cache_bust = EdgeCache::Bust.new
      cache_bust.call("/#{path}")
    end
  end
end
