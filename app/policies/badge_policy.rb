# @specre 01KJ6FFA2FH0HVDCGYH9XQB3GG
# @specre 01KJ6FB22VF10D4883F2B226HM
class BadgePolicy < ApplicationPolicy
  def api?
    user&.any_admin?
  end
end