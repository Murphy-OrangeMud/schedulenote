import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

<<<<<<< Updated upstream
Vue.config.productionTip = false

=======
>>>>>>> Stashed changes
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
<<<<<<< Updated upstream
=======

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) { // 验证是否需要登陆
    document.title = to.matched[0].meta.title
    next()
  } else {
    document.title = to.matched[0].meta.title
    next()
  }
})
>>>>>>> Stashed changes
