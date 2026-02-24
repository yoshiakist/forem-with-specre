# @specre 01KJ6FB22VF10D4883F2B226HM
class BadgeUploader < BaseUploader
  def extension_allowlist
    %w[jpg jpeg gif png webp]
  end
end
