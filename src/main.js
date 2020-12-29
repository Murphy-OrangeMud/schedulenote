import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueMarkdownEditor from '@kangc/v-md-editor'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import fullCalendar from 'vue-fullcalendar'

Vue.component('full-calendar', fullCalendar)
Vue.config.productionTip = false
VueMarkdownEditor.use(vuepressTheme)
Vue.use(ElementUI)
Vue.use(VueMarkdownEditor)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) { // 验证是否需要登陆
    document.title = to.matched[0].meta.title
    next()
  } else {
    document.title = to.matched[0].meta.title
    next()
  }
})
