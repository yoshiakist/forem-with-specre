# @specre 01KJ1C8G3AN3EVK907SGXDWZG5
class ImageUploadPolicy < ApplicationPolicy
  def create?
    !user.spam_or_suspended?
  end
end
