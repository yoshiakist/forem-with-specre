// @specre 01KJXW7T67VPX2HZKKWN70MM4E
import { h, render } from 'preact';
import { ListingDashboard } from '../listings/listingDashboard';

function loadElement() {
  const root = document.getElementById('listings-dashboard');
  if (root) {
    render(<ListingDashboard />, root);
  }
}

window.InstantClick.on('change', () => {
  loadElement();
});

loadElement();
