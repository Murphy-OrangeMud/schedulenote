<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
    <form>
        <div id="input">
            账号
            <input type="text" name="userid" placeholder="请输入你的账号">
            <br>
            密码
            <input type="password" name="userpassword" placeholder="请输入你的密码">
            <br>
            <h1></h1>
            <button v-on:click="loginCheck()">登录</button>
            <h1></h1>
            <router-link to="/register">注册账号</router-link>
        </div>
    </form>
  </div>
</template>

<script>
export default {
  methods: {
    register: function () {
      this.$router.push('/register')
    },
    loginCheck: function () {
      this.$router.push('/home')
    }
  }
}
</script>
