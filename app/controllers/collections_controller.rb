# @specre 01KJ6C1WBXTZN9GA5WYQPMQJSA
# @specre 01KJ6BZ9FHN72VNWP7JGG6DWBZ
class CollectionsController < ApplicationController
  def index
    @user = User.find_by!(username: params[:username])
    @collections = @user.collections.non_empty.order(created_at: :desc)
  end

  def show
    @collection = Collection.find(params[:id])
    @user = @collection.user
    @articles = @collection.articles.from_subforem.published.order(Arel.sql("COALESCE(crossposted_at, published_at) ASC"))
  end
end
