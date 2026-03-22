import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import MetricsView   from '../views/MetricsView.vue'
import InsightsView  from '../views/InsightsView.vue'

const routes = [
  { path: '/',         name: 'Dashboard', component: DashboardView },
  { path: '/metrics',  name: 'Metrics',   component: MetricsView },
  { path: '/insights', name: 'Insights',  component: InsightsView },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

export default createRouter({
  history: createWebHistory(),
  routes
})