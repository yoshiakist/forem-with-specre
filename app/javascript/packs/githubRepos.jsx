// @specre 01KHY99D5ZW1JPV9A0GAQGK90W
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
