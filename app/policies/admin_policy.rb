# @specre 01KJ9GW0HAGR8XG1KN5GETDK8Q
class AdminPolicy < ApplicationPolicy
  def show?
    user_super_admin?
  end

  def minimal?
    user_any_admin?
  end
end
