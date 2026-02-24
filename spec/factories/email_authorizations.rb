# @specre 01KJ759KKVVQ8YQZP1B78QC3Q6
FactoryBot.define do
  factory :email_authorization do
    user
    type_of { "merge_request" }
    json_data { { keep_user_id: 1, deleted_user_id: 1 } }
  end
end
