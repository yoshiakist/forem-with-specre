# @specre 01KHYDGFH91Y4CKRSK7XB9CAY2
FactoryBot.define do
  factory :survey do
    title { Faker::Lorem.word }
    active { true }
    display_title { true }
    allow_resubmission { false }
  end
end
