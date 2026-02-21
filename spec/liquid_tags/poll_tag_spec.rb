# @specre 01KHY7Q18QQ15B7XBT5YDRTEQ6
require "rails_helper"

RSpec.describe PollTag, type: :liquid_tag do
  describe ".user_authorization_method_name" do
    subject(:result) { described_class.user_authorization_method_name }

    it { is_expected.to eq(:any_admin?) }
  end
end
