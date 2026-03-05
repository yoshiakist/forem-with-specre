# @specre 01KHZKDENF1FEDNJQD6XXKWAKZ
# @specre 01KHZKCR70BAFQ159BEQFXBJQW
FactoryBot.define do
  factory :survey do
    title { Faker::Lorem.word }
    active { true }
    display_title { true }
    allow_resubmission { false }
  end
end
