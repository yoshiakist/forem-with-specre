# @specre 01KHZ69T25SN7PPC7HH7ZPCZ2D
class ProfilePreviewCardsController < ApplicationController
  layout false

  def show
    @user = User.includes(:profile, :setting).find(params[:id])
    set_cache_control_headers
    set_surrogate_key_header(*@user.profile_cache_keys)
  end
end
