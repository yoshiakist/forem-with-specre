# @specre 01KJBGZF9PRSHNVF807K57AY46
class SessionsController < Devise::SessionsController
  def destroy
    if user_signed_in?
      current_user.update_columns(current_sign_in_at: nil, current_sign_in_ip: nil)
      cookies.delete(:forem_user_signed_in, domain: request.host)
      super
    end
  end
end
