# @specre 01KJ6GMVW8YA3D7EE2WW7VZEZV
class AuditLog < ApplicationRecord
  belongs_to :user, optional: true

  validates :data, presence: true

  MODERATOR_AUDIT_LOG_CATEGORY = "moderator.audit.log".freeze
  ADMIN_API_AUDIT_LOG_CATEGORY = "admin_api.audit.log".freeze
end
