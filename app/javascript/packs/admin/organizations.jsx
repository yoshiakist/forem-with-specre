// @specre 01KHYB1FSJRAWD3J79MJ5ZA141
import { showOrganizationModal } from '././organizations/modals';
import { initializeDropdown } from '@utilities/dropdownUtils';

initializeDropdown({
  triggerElementId: 'options-dropdown-trigger',
  dropdownContentId: 'options-dropdown',
});

document.body.addEventListener('click', showOrganizationModal);
