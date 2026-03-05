// @specre 01KJ1SC2K2MHD1YYH79TBFM4VQ
import { h, render } from 'preact';
import { GithubRepos } from '../githubRepos/githubRepos';

function loadElement() {
  const root = document.getElementById('github-repos-container');
  if (root) {
    render(<GithubRepos />, root);
  }
}

window.InstantClick.on('change', () => {
  loadElement();
});

loadElement();
