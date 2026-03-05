// @specre 01KJ5DQT35P394JJVCSC077ZX5
import { embedGists } from '../utilities/gist';

const targetNode = document.querySelector('.comment-form');
targetNode && embedGists(targetNode);
