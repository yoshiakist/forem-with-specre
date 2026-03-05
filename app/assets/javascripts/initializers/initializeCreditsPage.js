// @specre 01KJ2SF6J4K95BTZRSZG5AA811
/* global localizeTimeElements */

'use strict';

function initializeCreditsPage() {
  const datetimes = document.querySelectorAll('.ledger time');

  localizeTimeElements(datetimes, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}
