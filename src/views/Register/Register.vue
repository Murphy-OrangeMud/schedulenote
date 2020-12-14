<template>
  <div id="login">
    <h1>Schedule note 用户注册</h1>
    <form>
        <div id="input">
            账号
            <input type="text" name="userid" placeholder="请输入你的账号" v-model=account>
            <br>
            <h1></h1>
            密码
            <input type="password" name="userpassword" placeholder="请输入你的密码" v-model=password>
            <br>
            <h1></h1>
            <button v-on:click="regi()">注册</button>
        </div>
        <div v-if="noteCount">
            <input type="text" name="userid" placeholder="请输入你的账号" v-model=mess>
        </div>
    </form>
  </div>
</template>

<script>
import { postRegister } from 'network/home'
export default {
  name: 'register',
  data () {
    return {
      account: '',
      password: '',
      mess: ''
    }
  },
  methods: {
    regi: function () {
      postRegister(this.account, this.password).then(res => {
        this.mess = res
      })
    }
  }
}
</script>
