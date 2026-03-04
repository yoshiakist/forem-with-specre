# @specre 01KJVE4GNV49HXNQ53W5PDJ31Z
# @specre 01KJVE2B3BE3E5GX1FAFCMEAEV
# @specre 01KJVDZDG8Y04Z6WRBBRCDEZGF
class StripeActiveCardPolicy < ApplicationPolicy
  def create?
    !user.spam_or_suspended?
  end

  alias update? create?

  def destroy?
    true
  end
end
