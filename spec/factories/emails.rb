# @specre 01KJ758K1CA5TWC5FHEKJZ52BT
FactoryBot.define do
  factory :email do
    subject { Faker::Lorem.sentence }
    body { Faker::Lorem.sentence }
    status { "active" }
  end
end
