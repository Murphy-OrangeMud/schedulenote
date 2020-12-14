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
        name: '软工笔记1',
        contributor: 'hzj',
        date: '2020-12-13',
        upvote: 100,
        downvote: 1
      },
      {
        course: '软件工程',
        name: '软工笔记2',
        contributor: 'hzj',
        date: '2020-12-13',
        upvote: 100,
        downvote: 1
      }
    ],
    courseList: [
      {
        course: '软件工程',
        contributor: 'skipher',
        time: '周二34，周四56'
      }
    ],
    materialList: [
      {
        course: '软件工程',
        name: '软工课件1',
        contributor: 'hzj',
        date: '2020-12-13',
        upvote: 100,
        downvote: 1
      },
      {
        course: '软件工程',
        name: '软工课件2',
        contributor: 'hzj',
        date: '2020-12-13',
        upvote: 100,
        downvote: 1
      }
    ],
    mdtext: 'markdown'
  },
  gatters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})

export default store
