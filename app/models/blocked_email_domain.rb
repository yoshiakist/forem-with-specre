# @specre 01KJVP4KGZFT0V02XDF80Y8517
# @specre 01KJ74FE48B8HJGBTKCFTWECFQ
# @specre 01KJ74CHA3SNK2FRMDYG1B7QA5
class BlockedEmailDomain < ApplicationRecord
  validates :domain, presence: true, uniqueness: true
  validates :domain,
            format: {
              with: /\A[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\z/, message: "must be a valid domain"
            }

  # Normalize domain to lowercase for consistent storage and comparison
  before_validation :normalize_domain

  # Check if a domain is blocked (exact match or subdomain match)
  # @param domain [String] The domain to check
  # @return [Boolean] true if the domain is blocked
  def self.blocked?(domain)
    return false if domain.blank?

    normalized_domain = domain.downcase.strip

    # Check for exact match
    return true if exists?(domain: normalized_domain)

    # Check for subdomain matches (e.g., if "example.com" is blocked, "sub.example.com" should also be blocked)
    blocked_domains = pluck(:domain)
    blocked_domains.any? { |blocked| normalized_domain.ends_with?(".#{blocked}") }
  end

  # Get all blocked domains as an array
  # @return [Array<String>] Array of blocked domain strings
  def self.domains
    pluck(:domain)
  end

  private

  def normalize_domain
    self.domain = domain&.downcase&.strip
  end
end
