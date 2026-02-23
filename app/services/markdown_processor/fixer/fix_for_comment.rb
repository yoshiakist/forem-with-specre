# @specre 01KJ2X9JEDPKB2DTN1GAMBQ254
module MarkdownProcessor
  module Fixer
    class FixForComment < Base
      METHODS = %i[
        underscores_in_usernames
      ].freeze
    end
  end
end
