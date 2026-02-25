# @specre 01KJ9JE1SPDCRJXAB1S3R7EKGT
require "rails_helper"

RSpec.describe UserLanguage do
  describe "validations" do
    subject { build(:user_language) }

    describe "builtin validations" do
      it { is_expected.to belong_to(:user) }
      it { is_expected.to validate_presence_of(:language) }
    end

    it "actually validates language" do
      expect(build(:user_language, language: :es)).to be_valid
    end

    it "actually validates language (invalid)" do
      lang = build(:user_language, language: :abracadabra)
      expect(lang).not_to be_valid
      expect(lang.errors[:language]).to be_present
    end
  end
end
