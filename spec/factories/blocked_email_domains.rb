# @specre 01KJ74CHA3SNK2FRMDYG1B7QA5
FactoryBot.define do
  factory :blocked_email_domain do
    domain { "example.com" }

    trait :with_subdomain do
      domain { "sub.example.com" }
    end

    trait :international do
      domain { "example.co.uk" }
    end

    trait :hyphenated do
      domain { "test-domain.com" }
    end
  end
end
