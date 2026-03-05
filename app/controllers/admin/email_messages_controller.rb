# @specre 01KJ758NKFTEQKYMBYPEGR3817
module Admin
  class EmailMessagesController < Admin::ApplicationController
    layout "admin"

    def show
      @user = User.find(params[:user_id])
      @email = EmailMessage.find(params[:id])
    end
  end
end
