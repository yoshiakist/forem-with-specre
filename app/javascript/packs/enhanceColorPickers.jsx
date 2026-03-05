// @specre 01KJXXT4W5WS018D6C53D3JFD6
import { replaceTextInputWithColorPicker } from '../colorPickers/replaceTextInputWithColorPicker';

// Find any color picker inputs on the page and replace them with the Preact enhanced component
const colorInputs = document.querySelectorAll('[data-color-picker]');

for (const input of colorInputs) {
  const { labelText } = input.dataset;
  replaceTextInputWithColorPicker({ input, labelText });
}
