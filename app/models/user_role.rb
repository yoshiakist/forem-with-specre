# @specre 01KJ7G7F0BZ5ZBSGWV365S2RYC
# @specre 01KJ7G7M4JRVA0J8VWAVJ7Y5ME
# Exposes the `rolify` gem's `users_roles` table via ActiveRecord
class UserRole < ApplicationRecord
  self.table_name = "users_roles"

  belongs_to :user
  belongs_to :role
end
