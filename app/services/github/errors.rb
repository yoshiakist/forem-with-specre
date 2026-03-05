# @specre 01KJ1SC2K2MHD1YYH79TBFM4VQ
module Github
  module Errors
    class Error < StandardError
    end

    class ClientError < Error
    end

    class ServerError < Error
    end

    class NotFound < ClientError
    end

    class Unauthorized < ClientError
    end

    class InvalidRepository < ArgumentError
    end

    class AccountSuspended < ClientError
    end

    class RepositoryUnavailable < ClientError
    end
  end
end
