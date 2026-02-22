# @specre 01KJ1ARF08DVRQE65SWASWAFWJ
FactoryBot.define do
  factory :mention do
    user
    association :mentionable, factory: :article
  end
end
