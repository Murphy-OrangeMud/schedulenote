import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    ddlList: [
      {
        date: '2020-12-13',
        course: '软件工程',
        task: '开会'
      },
      {
        date: '2020-12-19',
        course: '软件工程',
        task: '开会'
      }
    ],
    noteList: [
      {
        course: '软件工程',
        name: '软工笔记',
        contributor: 'hzj',
        date: '2020-12-13'
      },
      {
        course: '软件工程',
        name: '软工笔记2',
        contributor: 'hzj',
        date: '2020-12-13'
      }
    ],
    mdtext: 'markdown'
  },
  gatters: {
    ddlList (state) {
      return state.ddlList
    },
    ddlCount (state, getters) {
      return getters.ddlList.length
    }
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})

export default store
