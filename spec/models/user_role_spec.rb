# @specre 01KJ7G7F0BZ5ZBSGWV365S2RYC
# @specre 01KJ7G7M4JRVA0J8VWAVJ7Y5ME
require "rails_helper"

RSpec.describe UserRole do
  it { is_expected.to belong_to(:user) }
  it { is_expected.to belong_to(:role) }
end
