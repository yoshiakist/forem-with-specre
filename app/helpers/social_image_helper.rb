# @specre 01KJVEZN3YK9PYFVQ7FW9BBN7M
module SocialImageHelper
  def article_social_image_url(article, **options)
    Articles::SocialImage.new(article, **options).url
  end
end
