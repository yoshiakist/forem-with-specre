# @specre 01KJVE4GNV49HXNQ53W5PDJ31Z
# @specre 01KJVE2B3BE3E5GX1FAFCMEAEV
# @specre 01KJVDZDG8Y04Z6WRBBRCDEZGF
require "rails_helper"

RSpec.describe StripeActiveCardPolicy, type: :policy do
  subject { described_class.new(user, :stripe_active_card) }

  context "when user is not signed in" do
    let(:user) { nil }

    it { within_block_is_expected.to raise_error(Pundit::NotAuthorizedError) }
  end

  context "when user is signed in" do
    let(:user) { build(:user) }

    it { is_expected.to permit_actions(%i[create update destroy]) }

    context "when user is suspended" do
      let(:user) { build(:user, :suspended) }

      it { is_expected.to forbid_actions(%i[create update]) }
    end
  end
end
