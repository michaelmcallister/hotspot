import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  history: createWebHistory(),
  routes: [
    // 5.1 Core Discovery & Risk, Homepage & Search
    { path: '/', component: () => import('@/pages/HomePage.vue') },

    // 8.1 Core Discovery & Risk, Suburb Safety Report
    //{ path: '/suburb/:slug', component: () => import('@/pages/SuburbReportPage.vue') },

    // 4.1 Parking Search & Filters
    //{ path: '/parking', component: () => import('@/pages/ParkingSearchPage.vue') },

    // 4.1  Parking Spot Detail
    //{ path: '/parking/:id', component: () => import('@/pages/ParkingDetailPage.vue') },

    // 4.3 Saved/Favourite Spots
    //{ path: '/favourites', component: () => import('@/pages/FavoritesPage.vue') },

    // 4.1 Community Input, Suggest a Safe Spot
    //{ path: '/contribute', component: () => import('@/pages/ContributeSpotPage.vue') },

    // 4.2 Community Input, Suggestions Feed
    //{ path: '/community', component: () => import('@/pages/CommunityFeedPage.vue') },

    // 4.2 Community Input, Suggestion Detail
    //{ path: '/community/:id', component: () => import('@/pages/CommunityDetailPage.vue') },
  ],
})

