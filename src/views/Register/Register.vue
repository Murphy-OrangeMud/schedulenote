<template>
  <div id="login">
    <h1>Schedule note 用户注册</h1>
    <el-form ref=for :model="form" label-width="80px" class="login-form">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model=email></el-input>
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model=username></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model=password type="password"></el-input>
        </el-form-item>

        <el-form-item label="验证码" v-if=canvertified prop="verti">
          <el-input v-model=verti></el-input>
        </el-form-item>

        <el-form-item v-else>
          <el-button type=mess @click=regi>获取验证码</el-button>
        </el-form-item>
        <el-form-item v-if=canvertified>
          <el-button type=mess @click=regis>注册</el-button>
        </el-form-item>
      </el-form>
      <div v-if=mess>
        <el-tag type="success">{{mess}}</el-tag>
      </div>
  </div>
</template>

<script>
import { postRegister, searchEmail, getMailVertify, checkMailVertify } from 'network/home'
import qs from 'qs'
export default {
  name: 'register',
  data () {
    return {
      email: '',
      username: '',
      password: '',
      mess: '',
      checkmess: '',
      verti: ''
    }
  },
  computed: {
    canvertified: function () {
      return this.checkmess === 'Get verify code successfully'
    }
  },
  methods: {
    regis: function () {
      const vertidata = qs.stringify({
        email: this.email,
        verify_code: this.verti
      })
      console.log(vertidata)
      checkMailVertify(vertidata).then(res => {
        this.mess = res.data.msg
      })
      if (this.mess === 'Check verify code successfully') {
        const datas = qs.stringify({
          name: this.account,
          password: this.password,
          email: this.email
        })
        console.log(datas)
        postRegister(datas).then(res => {
          this.mess = res.data.msg
        })
      }
    },
    regi: function () {
      const emaildata = qs.stringify({
        email: this.email
      })
      console.log(emaildata)
      searchEmail(emaildata)
        .then((res) => {
          console.log(res)
          if (res.data.msg === 'success') {
            this.mess = 'Email already exist'
          } else {
            getMailVertify(emaildata).then((res) => {
              this.mess = res.data.msg
              this.checkmess = res.data.msg
            })
          }
        })
    }
  }
}
</script>
