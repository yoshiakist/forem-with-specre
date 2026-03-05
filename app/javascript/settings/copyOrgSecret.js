// @specre 01KHZ466X2VM8VAWD6RE82CF9J
export function copyToClipboardListener() {
  const settingsOrgSecretInput = document.getElementById('settings-org-secret');
  if (settingsOrgSecretInput === null) return;

  const { value } = settingsOrgSecretInput;
  return window.Forem.Runtime.copyToClipboard(value).then(() => {
    // Show the confirmation message
    document.getElementById('copy-text-announcer').classList.remove('hidden');
  });
}

export function setupCopyOrgSecret() {
  document
    .getElementById('settings-org-secret-copy-btn')
    ?.addEventListener('click', copyToClipboardListener);
}
