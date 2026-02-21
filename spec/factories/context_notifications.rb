# @specre 01KJ15YY7SWMF93P655KXRSPEK
FactoryBot.define do
  factory :context_notification do
    action { "Published" }
    association :context, factory: :article
  end
end
