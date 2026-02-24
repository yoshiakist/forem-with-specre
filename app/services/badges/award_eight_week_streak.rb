# @specre 01KJ6FJWX16YC4Y1JXWM0A595S
module Badges
  class AwardEightWeekStreak
    def self.call
      ::Badges::AwardStreak.call(weeks: 8)
    end
  end
end
