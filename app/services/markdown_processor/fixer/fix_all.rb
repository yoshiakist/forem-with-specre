# @specre 01KJ2X9JEDPKB2DTN1GAMBQ254
module MarkdownProcessor
  module Fixer
    class FixAll < Base
      METHODS = %i[
        add_quotes_to_title
        add_quotes_to_description
        lowercase_published
        convert_new_lines
        split_tags
        underscores_in_usernames
      ].freeze
    end
  end
end
