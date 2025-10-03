import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../Homepage.vue'
import TopSuburbs from '../TopSuburbs.vue'
import Saved from '../Saved.vue'
import Contact from '../Contact.vue'
import NotFound from '../NotFound.vue'

const routes = [
  { path: '/', name: 'home', component: Homepage },
  { path: '/suburb/:slug', name: 'suburb', component: Homepage, props: true },
  { path: '/top-suburbs', name: 'top-suburbs', component: TopSuburbs },
  { path: '/saved', name: 'saved', component: Saved },
  { path: '/contact', name: 'contact', component: Contact },
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

