# @specre 01KJ9GW0HAGR8XG1KN5GETDK8Q
class InternalPolicy < ApplicationPolicy
  def access?
    user.administrative_access_to?(resource: record)
  end
end
