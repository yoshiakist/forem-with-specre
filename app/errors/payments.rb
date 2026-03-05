# @specre 01KJVE4GNV49HXNQ53W5PDJ31Z
# @specre 01KJVE2B3BE3E5GX1FAFCMEAEV
# @specre 01KJ2SF6J4K95BTZRSZG5AA811
# @specre 01KJVDZDG8Y04Z6WRBBRCDEZGF
module Payments
  class PaymentsError < StandardError
  end

  class InvalidRequestError < PaymentsError
  end

  class CardError < PaymentsError
  end
end
