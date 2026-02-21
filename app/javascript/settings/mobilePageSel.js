// @specre 01KHZ466X2VM8VAWD6RE82CF9J
export function mobilePageSelListener(event) {
  const url = event.target.value;
  InstantClick.preload(url);
  InstantClick.display(url);
}

export function setupMobilePageSel() {
  document
    .getElementById('mobile-page-selector')
    ?.addEventListener('change', mobilePageSelListener);
}
