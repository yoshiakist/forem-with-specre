# @specre 01KHYCN1D8NN3GXYBG17C9P3XV
module Tags
  class BustCacheWorker < BustCacheBaseWorker
    def perform(tag_name)
      tag = Tag.find_by(name: tag_name)
      return unless tag

      EdgeCache::BustTag.call(tag)
    end
  end
end
