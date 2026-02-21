// @specre 01KJ15MVQ9HCZ8PV80MQ828AQF
import { embedGists } from '../utilities/gist';

function handleEmbedGists() {
  const targetNode = document.querySelector('#articles-list');
  targetNode && embedGists(targetNode);
}

window.InstantClick.on('change', () => {
  handleEmbedGists();
});

handleEmbedGists();
