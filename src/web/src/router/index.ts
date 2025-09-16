import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../Homepage.vue'
import TopSuburbs from '../TopSuburbs.vue'
import NotFound from '../NotFound.vue'

const routes = [
  { path: '/', name: 'home', component: Homepage },
  { path: '/top-suburbs', name: 'top-suburbs', component: TopSuburbs },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router

