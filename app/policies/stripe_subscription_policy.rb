# @specre 01KJVE2459NGVYNN0C6XT6TMSM
# @specre 01KJVDZ0VWPAMMPR1QMC4D1Q8P
# @specre 01KJVDW17MZNP820R66MDD04E5
class StripeSubscriptionPolicy < ApplicationPolicy
  def create?
    !user.spam_or_suspended?
  end

  alias update? create?

  def destroy?
    true
  end
end
