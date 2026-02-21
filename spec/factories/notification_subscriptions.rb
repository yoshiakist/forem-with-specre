# @specre 01KJ15N9VC5VXN9692QKQRVF5E
FactoryBot.define do
  factory :notification_subscription do
    user
    association :notifiable, factory: :article
  end
end
