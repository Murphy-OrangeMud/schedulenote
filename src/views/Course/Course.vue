<template>
  <div id="calender">
    <h1>课程列表</h1>
    <div v-if="courseCount">
      <table align="center">
        <thead>
          <tr>
            <th>时间</th>
            <th>课程</th>
            <th>笔记</th>
            <th>资料</th>
            <th>操作</th>
          </tr>
        </thead>
      <tbody>
        <tr v-for="item in courseList" :key="item" >
        <td>{{item.time}}</td>
        <td>{{item.course}}</td>
        <td><button v-on:click="chooseNote()">查询</button></td>
        <td><button v-on:click="chooseMaterials()">查询</button></td>
        <td><button v-on:click="deleteCourse()">删除</button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>课程为空</h2>
    <h1></h1>
    <button v-on:click="addCourse()">添加课程</button>
    <button v-on:click="refresh()">刷新</button>
  </div>
</template>

<script>
export default {
  name: 'course',
  computed: {
    courseList () {
      return this.$store.state.courseList
    },
    courseCount () {
      // console.log(this.$store.state.courseList)
      return this.$store.state.courseList.length
    }
  },
  methods: {
    chooseNote () {
      this.$router.push('/notes')
    },
    chooseMaterials () {
      this.$router.push('/materials')
    },
    addCourse () {
      // check admin
    },
    deleteCourse () {
      // check admin
    },
    refresh: function () {
      this.$axios.defaults.baseURL = 'http://localhost:8080/api'
      this.$axios.get('/api/getDDL')
        .then((response) => {
          console.log(response)
        })
    }
  }
}
</script>

<style>
table {
  border: 1px solid #e9e9e9;
  border-collapse: collapse;
  border-spacing: 0;
}

th, td {
  padding: 8px 16px;
  border: 1px solid #e9e9e9;
  text-align: left;
}

th {
  background-color: #f7f7f7;
  color: #5c6b77;
  font-weight: 600;
}
</style>
