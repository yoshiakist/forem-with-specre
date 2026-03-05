// @specre 01KJ9GWWKF62PQBKP13K74MPN0
import { Controller } from '@hotwired/stimulus';

export default class NoticeController extends Controller {
  static targets = ['noticeZone'];

  closeNotice() {
    document.getElementById('notice-container').addEventListener('click', (event) => {
      event.preventDefault();
      document.getElementById('notice-container').remove();
    })
  }
}
