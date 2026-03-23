import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import MetricsView   from '../views/MetricsView.vue'
import InsightsView  from '../views/InsightsView.vue'
import LoginView     from '../views/LoginView.vue'

const routes = [
  { path: '/login', name: 'Login', component: LoginView, meta: { public: true } },
  { path: '/',         name: 'Dashboard', component: DashboardView },
  { path: '/metrics',  name: 'Metrics',   component: MetricsView },
  { path: '/insights', name: 'Insights',  component: InsightsView },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (!to.meta.public && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router