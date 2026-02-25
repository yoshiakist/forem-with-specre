# @specre 01KJ9K792FM0FA2QSE1BE6N7AE
FactoryBot.define do
  factory :user_block do
    association :blocker, factory: :user
    association :blocked, factory: :user
    config { "default" }
  end
end
