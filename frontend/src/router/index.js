import { createRouter, createWebHistory } from 'vue-router'

import BatchProcess from '../views/BatchProcess.vue'
import Detail from '../views/Detail.vue'
import History from '../views/History.vue'
import Home from '../views/Home.vue'
import Statistics from '../views/Statistics.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/batch', name: 'batch-process', component: BatchProcess },
    { path: '/history', name: 'history', component: History },
    { path: '/detail/:id', name: 'detail', component: Detail, props: true },
    { path: '/statistics', name: 'statistics', component: Statistics },
  ],
})

export default router
