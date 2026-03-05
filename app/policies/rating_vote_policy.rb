# @specre 01KJVS4H4SB05PGMMFNHGWXVV4
class RatingVotePolicy < ApplicationPolicy
  def create?
    !user.spam_or_suspended?
  end

  def permitted_attributes
    %i[rating group article_id]
  end
end
