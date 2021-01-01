import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    id: 0,
    username: '',
    email: '',
    password: '',
    avatar: '',
    motto: '',
    is_admin: false,
    ddlList: [
      {
        title: '软工开会',
        start: '2020-12-12',
        end: '2020-12-13'
      },
      {
        title: '软工开会',
        start: '2020-12-19',
        end: '2020-12-20'
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
        coursename: '软件工程',
        filename: '软工课件1',
        uploader: 'hzj',
        date: '2020-12-13',
        score: 100,
        downvote: 1
      },
      {
        coursename: '软件工程',
        filename: '软工课件2',
        uploader: 'hzj',
        date: '2020-12-13',
        score: 100,
        downvote: 1
      }
    ],
    mdtext: 'markdown'
  }
})

export default store
