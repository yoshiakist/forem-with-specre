# @specre 01KJBV508Z7X8FZ7BZP7XQNTN1
FactoryBot.define do
  factory :page_view do
    user
    article
    referrer { Faker::Internet.url }
  end
end
