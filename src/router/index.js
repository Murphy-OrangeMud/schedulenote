import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    meta: {
      requireAuth: true // 配置此条，进入页面前判断是否需要登陆
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/calender',
    name: 'Calender',
    meta: {
      requireAuth: true // 配置此条，进入页面前判断是否需要登陆
    },
    component: () => import('../views/Calender.vue')
  },
  {
    path: '/home',
    name: 'Home',
    meta: {
      requireAuth: true // 配置此条，进入页面前判断是否需要登陆
    },
    component: () => import('../views/Home.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
