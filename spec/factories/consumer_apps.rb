# @specre 01KJ3YXYAR6AARATJH02XHAEVW
FactoryBot.define do
  factory :consumer_app do
    auth_key { Faker::Alphanumeric.alpha(number: 10) }
    active { true }
    platform { :ios }
    app_bundle { Faker::Internet.domain_name(subdomain: true) }
  end
end
