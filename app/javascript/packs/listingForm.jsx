// @specre 01KJXWGP0V021QH50BJW9Q1KKD
// @specre 01KJXWGTKXY2KHWQQ23XG2PNZF
import { h, render } from 'preact';
import { ListingForm } from '../listings/listingForm';

function loadElement() {
  const root = document.getElementById('listingform-data');
  if (root) {
    const {
      listing,
      organizations,
      categoriesForSelect,
      categoriesForDetails,
    } = root.dataset;
    render(
      <ListingForm
        organizations={organizations}
        listing={listing}
        categoriesForSelect={categoriesForSelect}
        categoriesForDetails={categoriesForDetails}
      />,
      root,
    );
  }
}

window.InstantClick.on('change', () => {
  loadElement();
});

loadElement();
