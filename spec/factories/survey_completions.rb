# @specre 01KHYDHRP7XCMAJFEZ27YPZK5Y
FactoryBot.define do
  factory :survey_completion do
    user
    survey
    completed_at { Time.current }
  end
end
