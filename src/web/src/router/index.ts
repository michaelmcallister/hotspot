import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../Homepage.vue'
import TopSuburbs from '../TopSuburbs.vue'
import Saved from '../Saved.vue'
import Contact from '../Contact.vue'
import Settings from '../Settings.vue'
import NotFound from '../NotFound.vue'

const routes = [
  { path: '/', name: 'home', component: Homepage },
  { path: '/suburb/:slug', name: 'suburb', component: Homepage, props: true },
  { path: '/explore', name: 'explore', component: TopSuburbs },
  { path: '/saved', name: 'saved', component: Saved },
  { path: '/contact', name: 'contact', component: Contact },
  { path: '/settings', name: 'settings', component: Settings },
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
