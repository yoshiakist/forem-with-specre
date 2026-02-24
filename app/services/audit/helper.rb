# @specre 01KJ162FSS39965A6QK4V78F2H
# @specre 01KJ6GMNB25T18H7JGRZFEBQH5
module Audit
  module Helper
    NOTIFICATION_SUFFIX = ".audit.log".freeze

    def instrument_name(name)
      "#{name}#{NOTIFICATION_SUFFIX}"
    end
  end
end
