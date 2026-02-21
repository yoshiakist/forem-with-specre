# @specre 01KHYYH62ZG383CA1EG815V11C
FactoryBot.define do
  factory :subforem do
    sequence(:domain) { |n| "subforem-#{n}.test" }
  end
end