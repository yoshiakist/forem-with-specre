# @specre 01KJ15MVQ9HCZ8PV80MQ828AQF
FactoryBot.define do
  factory :notification do
    association :user, factory: :user, strategy: :create
    association :organization, factory: :organization, strategy: :create
    notifiable { create(:article) }
  end
end
