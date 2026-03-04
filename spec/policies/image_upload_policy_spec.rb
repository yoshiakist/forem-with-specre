# @specre 01KJ1C8G3AN3EVK907SGXDWZG5
require "rails_helper"

RSpec.describe ImageUploadPolicy, type: :policy do
  subject { described_class.new(user, image) }

  let(:image) { "📸.jpg" }

  context "when user is not signed in" do
    let(:user) { nil }

    it { within_block_is_expected.to raise_error(Pundit::NotAuthorizedError) }
  end

  context "when user is signed in" do
    let(:user) { build_stubbed(:user) }

    it { is_expected.to permit_actions(%i[create]) }

    context "when user is suspended" do
      let(:user) { build(:user, :suspended) }

      it { is_expected.to forbid_actions(%i[create]) }
    end
  end
end
