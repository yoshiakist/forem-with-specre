# @specre 01KJ6GMNB25T18H7JGRZFEBQH5
module Audit
  class Subscribe
    class << self
      include Audit::Helper

      def listen(*listeners)
        listeners.each do |listener|
          ActiveSupport::Notifications.subscribe(instrument_name(listener)) do |*args|
            Audit::Notification.listen(*args)
          end
        end
      end

      def forget(*listeners)
        listeners.each { |listener| ActiveSupport::Notifications.unsubscribe(instrument_name(listener)) }
      end
    end
  end
end
