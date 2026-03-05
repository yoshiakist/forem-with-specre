// @specre 01KJ24JHMGN7PEYMPPQ31D9D2V
import('../previewCards/feedPreviewCards').then(
  ({ initializeFeedPreviewCards, listenForHoveredOrFocusedStoryCards }) => {
    initializeFeedPreviewCards();
    listenForHoveredOrFocusedStoryCards();
  },
);
