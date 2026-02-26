# @specre 01KJBWMN1X7QK4TMQ77F5NFR6E
class PinnedArticlePolicy < ApplicationPolicy
  def show?
    user&.any_admin?
  end

  alias update? show?

  alias destroy? show?
end
