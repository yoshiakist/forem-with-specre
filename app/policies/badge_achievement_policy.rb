# @specre 01KJ6FJA4XS9P5A266ZFW6Q7Y4
class BadgeAchievementPolicy < ApplicationPolicy
  def api?
    user&.any_admin?
  end
end