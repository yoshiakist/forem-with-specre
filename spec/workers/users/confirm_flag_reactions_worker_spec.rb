# @specre 01KHZ55S8Z1A16PNGY9X7PR58P
require "rails_helper"

RSpec.describe Users::ConfirmFlagReactionsWorker, type: :worker do
  describe "#perform" do
    let(:user) { create(:user) }
    let(:worker) { subject }

    it "calls spam reports resolver" do
      allow(Users::ConfirmFlagReactions).to receive(:call).with(user)

      worker.perform(user.id)
      expect(Users::ConfirmFlagReactions).to have_received(:call).with(user)
    end

    it "doesn't fail with invalid url" do
      worker.perform(-1)
    end
  end
end
