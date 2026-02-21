// @specre 01KHZ466X2VM8VAWD6RE82CF9J
import { setupCopyOrgSecret } from '../../settings/copyOrgSecret';
import { setupRssFetchTime } from '../../settings/rssFetchTime';
import { setupMobilePageSel } from '../../settings/mobilePageSel';

export function initializeSettings() {
  setupCopyOrgSecret();
  setupRssFetchTime();
  setupMobilePageSel();
}
