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
        <td>{{item.info}}</td>
        <td>{{item.name}}</td>
        <td><el-button v-on:click="chooseNote()" round type="success">查询</el-button></td>
        <td><el-button v-on:click="chooseMaterials(item.id)" round type="success">查询</el-button></td>
        <td><el-button v-on:click="deleteCourse(item.id)" round type="danger" >删除</el-button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>课程为空</h2>
    <h1></h1>
    <el-form ref=for label-width="80px" class="login-form">
      <el-form-item label="课程名称" prop="username">
        <el-input v-model="mycourse.name"></el-input>
      </el-form-item>

      <el-form-item label="课程时间" prop="username">
        <el-input v-model="mycourse.info"></el-input>
      </el-form-item>
    </el-form>
    <el-button v-on:click="addCourse()" type="primary" round>添加课程</el-button>
    <el-button v-on:click="refresh()" icon="el-icon-refresh" round>刷新</el-button>
  </div>
</template>

<script>
import { addcourse, getcourse, deletecourse } from 'network/home'
export default {
  name: 'course',
  data () {
    return {
      mycourse: {
        info: '',
        name: ''
      },
      mess: '未能获取ddl',
      courseList: [],
      courseCount: 0
    }
  },
  methods: {
    chooseNote () {
      this.$router.push('/notes')
    },
    chooseMaterials (ID) {
      this.$store.state.courseid = ID
      this.$router.push('/materials')
    },
    addCourse () {
      // check admin
      var formData = new FormData()
      formData.append('name', this.mycourse.name)
      formData.append('info', this.mycourse.info)

      addcourse(formData).then(res => {
        console.log(res)
      })
      getcourse(new FormData()).then(res => {
        this.courseList = res
        this.courseCount = res.length
      })
    },
    deleteCourse (id) {
      // check admin
      var formData = new FormData()
      formData.append('id', id)

      deletecourse(formData).then(res => {
        console.log(res)
      })
      getcourse(new FormData()).then(res => {
        this.courseList = res
        this.courseCount = res.length
      })
    },
    refresh: function () {
      getcourse(new FormData()).then(res => {
        this.courseList = res
        this.courseCount = res.length
      })
    }
  },
  created () {
    getcourse(new FormData()).then(res => {
      this.courseList = res
      this.courseCount = res.length
    })
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
