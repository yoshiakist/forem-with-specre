# @specre 01KJ2472X584A2R8VP2QAC7V40
module Articles
  module Feeds
    module Tag
      def self.call(tag = nil, number_of_articles: Article::DEFAULT_FEED_PAGINATION_WINDOW_SIZE, page: 1)
        articles =
          if tag.present?
            ::Tag.find_by(name: tag).articles
          else
            Article.all
          end

        articles
          .published
          .limited_column_select
          .includes(:distinct_reaction_categories, :context_notes)
          .page(page)
          .per(number_of_articles)
      end
    end
  end
end
