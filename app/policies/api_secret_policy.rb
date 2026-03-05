# @specre 01KJ9MTNQVSA7QWHW4VYYX71M4
class ApiSecretPolicy < ApplicationPolicy
  def create?
    !user.spam_or_suspended?
  end

  def destroy?
    user_owner?
  end

  def permitted_attributes
    %i[description]
  end

  private

  def user_owner?
    user.id == record.user_id
  end
end
