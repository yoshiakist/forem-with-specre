# @specre 01KJ9KAPX00THEMPV2WXQE43HT
# @specre 01KJ9K792FM0FA2QSE1BE6N7AE
class UserBlockPolicy < ApplicationPolicy
  def create?
    !user.spam_or_suspended?
  end

  alias destroy? create?

  def permitted_attributes
    %i[id blocked_id]
  end
end
