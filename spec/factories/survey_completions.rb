# @specre 01KHZKDENF1FEDNJQD6XXKWAKZ
FactoryBot.define do
  factory :survey_completion do
    user
    survey
    completed_at { Time.current }
  end
end
