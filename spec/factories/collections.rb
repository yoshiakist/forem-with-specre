# @specre 01KJ6C4VF5JP25A07CJA19PQHX
# @specre 01KJ6C1WBXTZN9GA5WYQPMQJSA
# @specre 01KJ6BZ9FHN72VNWP7JGG6DWBZ
FactoryBot.define do
  factory :collection do
    user
    sequence(:slug) { |n| "slug-#{n}" }
  end

  trait :with_articles do
    transient do
      amount { 3 }
    end
    after(:create) do |collection, evaluator|
      create_list(:article, evaluator.amount, with_collection: collection, user: collection.user)
    end
  end
end
