<template>
  <div id="app">
    <el-button type="primary" icon="el-icon-edit" @click="EnterWriting">笔记</el-button>
    <el-button type="primary" icon="el-icon-user" @click="ToReg">注册</el-button>
    <el-button type="primary" icon="el-icon-user-solid" @click="ToLogin">登陆</el-button>
    <el-button type="primary" icon="el-icon-date" @click="ToCal">日历</el-button>
    <el-button type="primary" icon="el-icon-date" @click="ToCourse">课程</el-button>
    <!--<el-button type="primary" icon="el-icon-folder" @click="ToNotes">笔记库</el-button>
    <el-button type="primary" icon="el-icon-folder" @click="ToMaterials">课程资料</el-button>-->
    <el-button type="primary" icon="el-icon-info" @click="ToAbout">关于</el-button>
    <el-button type="primary" icon="el-icon-userpage" @click="ToUserpage">个人主页</el-button>
    <router-view />
  </div>
</template>

<style>
@import "assets/css/normalize.css";
@CrossOrigin;

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*background-color: #99ffff;*/
  /* hys contributor */
}
.note{
  text-align: left;
}

</style>

<script>

export default {
  name: 'app',
  methods: {
    EnterWriting: function () {
      this.$router.push('/home')
    },
    ToReg: function () {
      this.$router.push('/register')
    },
    ToLogin: function () {
      this.$router.push('/login')
    },
    ToCal: function () {
      this.$router.push('/calender')
    },
    ToAbout: function () {
      this.$router.push('/about')
    },
    ToCourse: function () {
      this.$router.push('/course')
    },
    ToNotes: function () {
      this.$router.push('/notes')
    },
    ToMaterials: function () {
      this.$router.push('/materials')
    },
    ToUserpage: function () {
      this.$router.push('/Userpage')
    }
  }
}
</script>
