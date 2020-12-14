<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
    <el-form ref=for :model="form" label-width="80px" class="login-form">

        <el-form-item label="用户名" prop="username">
          <el-input v-model=account></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model=password type="password"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type=mess @click=regi>登录</el-button>
        </el-form-item>
      </el-form>
      <div v-if=mess>
        <el-tag type="success">{{mess}}</el-tag>
      </div>
  </div>
</template>

<script>
import { postLogin } from 'network/home'
import qs from 'qs'
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
      const datas = qs.stringify({
        name: this.account,
        password: this.password,
        email: '12345678@pku.edu.cn'
      })
      console.log(datas)
      event.preventDefault()
      postLogin(datas).then(res => {
        this.mess = res.data.msg
      })
    }
  }
}
</script>
