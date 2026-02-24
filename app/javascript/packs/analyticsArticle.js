// @specre 01KJ6QCAKAT1EKMN80R2KK58YZ
import { initCharts } from '../analytics/dashboard';

function initDashboardArticle() {
  const article = document.getElementById('article');
  const { articleId, organizationId } = article.dataset;
  initCharts({ articleId, organizationId });
}

window.InstantClick.on('change', () => {
  initDashboardArticle();
});

initDashboardArticle();
