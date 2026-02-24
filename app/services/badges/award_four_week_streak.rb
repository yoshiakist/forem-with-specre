# @specre 01KJ6FJWX16YC4Y1JXWM0A595S
module Badges
  class AwardFourWeekStreak
    def self.call
      ::Badges::AwardStreak.call(weeks: 4)
    end
  end
end
