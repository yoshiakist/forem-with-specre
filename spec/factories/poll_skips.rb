# @specre 01KHZMED56WYNARJ0KFNWFZHZX
FactoryBot.define do
  factory :poll_skip do
    poll
    user
    session_start { 0 }
  end
end
