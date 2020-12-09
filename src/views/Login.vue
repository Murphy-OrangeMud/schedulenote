<template>
  <div class="login">
    <h1>Schedule note 用户登录</h1>
    <form>
        <div id="input">
            学工号
            <input type="text" name="userid" placeholder="请输入你的北大学工号">
            <br>
            登录密码
            <input type="password" name="userpassword" placeholder="请输入你的登录密码">
            <br>
            <button v-on:click="loginCheck()">登录</button>
        </div>
    </form>
  </div>
</template>

export default {
  data () {

  },
  methods:{
   loginCheck:function(){
    alert(11111111111111111111)
    }
   }
 }
