<template>
  <div id="login">
    <h1>Schedule note 用户注册</h1>
    <form>
        <div id="input">
            账号
            <input type="text" name="userid" placeholder="请输入你的账号">
            <br>
            密码
            <input type="password" name="userpassword" placeholder="请输入你的密码">
            <br>
            <h1></h1>
            <button v-on:click="regi()">注册</button>
        </div>
    </form>
  </div>
</template>

<script>
export default {
  methods: {
    regi: function () {
      this.$router.push('/login')
    }
  }
}
</script>
