// @specre 01KJ5DQT35P394JJVCSC077ZX5
import { addLocalizedDateTimeToElementsTitles } from "../../utilities/localDateTime";

export function initializeCommentDate() {
  const commentsDates = document.querySelectorAll('.comment-date time');

  if (commentsDates) {
    addLocalizedDateTimeToElementsTitles(commentsDates, 'datetime');
  }
}
