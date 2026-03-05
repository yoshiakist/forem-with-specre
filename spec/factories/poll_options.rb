# @specre 01KHZMA857XQ0MP5F9S9D2ZYCX
FactoryBot.define do
  factory :poll_option do
    poll
    markdown { Faker::Hipster.words(number: 3) }
    supplementary_text { nil }
    position { 0 }
  end
end
