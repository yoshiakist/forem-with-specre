# @specre 01KJ6T0E5ZHZPXH2FM05E4X6Q6
class AiImageGenerationPolicy < ApplicationPolicy
  def create?
    # All users can generate AI images (as long as they're not spam)
    !user.spam
  end
end

