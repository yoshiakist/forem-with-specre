# @specre 01KHZ6GG5GD766PRZK1SE50KMG
module Images
  module ProfileImageGenerator
    def self.call
      Rails.root.join("app/assets/images/#{rand(1..40)}.png").open
    end
  end
end
