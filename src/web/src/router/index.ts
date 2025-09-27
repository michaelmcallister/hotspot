import { createRouter, createWebHistory } from 'vue-router';

import Contact from '../Contact.vue';
import Homepage from '../Homepage.vue';
import NotFound from '../NotFound.vue';
import Saved from '../Saved.vue';
import Settings from '../Settings.vue';
import TopSuburbs from '../TopSuburbs.vue';

const routes = [
  { path: '/', name: 'home', component: Homepage },
  { path: '/suburb/:slug', name: 'suburb', component: Homepage, props: true },
  { path: '/top-suburbs', name: 'top-suburbs', component: TopSuburbs },
  { path: '/saved', name: 'saved', component: Saved },
  { path: '/contact', name: 'contact', component: Contact },
  { path: '/settings', name: 'settings', component: Settings },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});

export default router;
