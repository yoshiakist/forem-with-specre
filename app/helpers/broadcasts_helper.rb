# @specre 01KJ6DW7GBQ5XAQKBV7MCPS2FA
# @specre 01KJ6DVV4TY3RHBN045KGH5ZXY
# @specre 01KJ6D7FQ3E8XSXDJQS2EYZTJ8
module BroadcastsHelper
  def banner_class(broadcast)
    return if broadcast.banner_style.blank?

    if broadcast.banner_style == "default"
      "crayons-banner"
    else
      "crayons-banner crayons-banner--#{broadcast.banner_style}"
    end
  end

  def sanitized_broadcast_id(broadcast_title)
    broadcast_title.downcase.delete(":").tr(" ", "_")
  end
end
