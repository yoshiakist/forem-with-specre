# @specre 01KJV9KZR85C73CRV2F1MZ7RN8
# @specre 01KJV9M0QR6H05KCHZ72V7A2BZ
# @specre 01KJV9M130S6RWDXS6V4WXKBGM
# @specre 01KJV9M1GJDQF9EFPNG89BSKVB
require "rails_helper"

RSpec.describe "ArticlesFeed" do
  let!(:article) { create(:article) }

  it "returns an rss feed with published articles" do
    get "/feed"

    expect(response.body).to include(article.title)
    expect(response.body).to include("<pubDate>#{article.published_at.to_fs(:rfc822)}</pubDate>")
  end
end
