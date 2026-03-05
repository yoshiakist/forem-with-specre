# @specre 01KJ6FJWX16YC4Y1JXWM0A595S
module Badges
  class AwardSixteenWeekStreak
    def self.call
      ::Badges::AwardStreak.call(weeks: 16)
    end
  end
end
