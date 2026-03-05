// @specre 01KJXXQCH4J8E98SGR04CZ6DK3
import { hideBlockedContent } from '../contentDisplayPolicy/hideBlockedContent';
import { initHiddenComments } from '../contentDisplayPolicy/initHiddenComments';

window.InstantClick.on('change', () => {
  hideBlockedContent();
  initHiddenComments();
});

hideBlockedContent();
initHiddenComments();
