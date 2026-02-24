# @specre 01KJ6GMVW8YA3D7EE2WW7VZEZV
FactoryBot.define do
  factory :audit_log do
    category { Faker::Name.name }
    slug     { Faker::Creature::Animal }
    data     { { action: Faker::ProgrammingLanguage.name, controller: Faker::Lorem.word } }
  end
end
