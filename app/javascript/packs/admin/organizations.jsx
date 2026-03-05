// @specre 01KJ02MNP5AREF4M1SM48V0ED6
import { showOrganizationModal } from '././organizations/modals';
import { initializeDropdown } from '@utilities/dropdownUtils';

initializeDropdown({
  triggerElementId: 'options-dropdown-trigger',
  dropdownContentId: 'options-dropdown',
});

document.body.addEventListener('click', showOrganizationModal);
