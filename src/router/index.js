import Vue from 'vue'
import VueRouter from 'vue-router'
<<<<<<< Updated upstream
import Home from '../views/Home.vue'
=======
>>>>>>> Stashed changes

Vue.use(VueRouter)

const routes = [
  {
<<<<<<< Updated upstream
    path: '/',
    name: 'Home',
    component: Home
=======
    path: '',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    meta: {
      title: 'login',
      requireAuth: false
    },
    component: () => import('../views/Login/Login.vue')
>>>>>>> Stashed changes
  },
  {
    path: '/about',
    name: 'About',
<<<<<<< Updated upstream
=======
    meta: {
      title: 'about',
      requireAuth: true
    },
>>>>>>> Stashed changes
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/About/About.vue')
  },
  {
<<<<<<< Updated upstream
    path: '/test',
    name: 'Test',
    component: () => import('../views/Test.vue')
=======
    path: '/calender',
    name: 'Calender',
    meta: {
      title: 'calender',
      requireAuth: true
    },
    component: () => import('../views/Calender/Calender.vue')
  },
  {
    path: '/home',
    name: 'Home',
    meta: {
      title: 'home',
      requireAuth: true
    },
    component: () => import('../views/Home/Home.vue')
  },
  {
    path: '/register',
    name: 'Register',
    meta: {
      title: 'register',
      requireAuth: false
    },
    component: () => import('../views/Register/Register.vue')
  },
  {
    path: '/notes',
    name: 'Notes',
    meta: {
      title: 'notes',
      requireAuth: false
    },
    component: () => import('../views/Notes/Notes.vue')
>>>>>>> Stashed changes
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
