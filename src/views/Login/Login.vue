<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
    <template>
      <el-radio v-model="radio" label="1">用户名登录</el-radio>
      <el-radio v-model="radio" label="">邮箱登录</el-radio>
    </template>
    <el-form ref=for :model="form" label-width="80px" class="login-form">

        <el-form-item v-if=radio label="用户名" prop="username">
          <el-input v-model=username></el-input>
        </el-form-item>

        <el-form-item v-else label="邮箱" prop="username">
          <el-input v-model=email></el-input>
        </el-form-item>

        <el-form-item v-if=radio label="密码" prop="password">
          <el-input v-model=password type="password"></el-input>
        </el-form-item>
        <el-form-item v-else label="验证码" prop="password">
          <el-input v-model=verti type="password"></el-input>
        </el-form-item>
        <el-form-item v-if=radio>
          <el-button type=mess @click=login>登录</el-button>
        </el-form-item>
        <el-form-item v-else-if=!canvertified >
          <el-button type=mess @click=getVerti>获取验证码</el-button>
        </el-form-item>
        <el-form-item v-else >
          <el-button type=mess @click=checkVerti>登录</el-button>
        </el-form-item>
      </el-form>
      <div v-if=mess>
        <el-tag type="success">{{mess}}</el-tag>
      </div>
  </div>
</template>

<script>
import { postLogin, searchEmail, getMailVertify, checkMailVertify, loginByEmail } from 'network/home'
import qs from 'qs'

export default {
  name: 'register',
  data () {
    return {
      radio: '',
      username: '',
      email: '',
      password: '',
      mess: '',
      verti: '',
      checkmess: ''
    }
  },
  computed: {
    canvertified: function () {
      return this.checkmess === 'Get verify code successfully'
    }
  },
  methods: {
    login: function () {
      const datas = qs.stringify({
        name: this.account,
        password: this.password
      })
      console.log(datas)
      event.preventDefault()
      postLogin(datas).then(res => {
        this.mess = res.data.msg
        console.log(res.data)
        if (this.mess === 'User "' + this.account + '" login success') {
          this.$store.state.id = res.data.id
          this.$store.state.username = res.data.username
          this.$store.state.motto = res.data.motto
          this.$store.state.password = this.password
          this.$store.state.is_admin = res.data.is_admin
        }
      })
    },
    getVerti: function () {
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
    },
    checkVerti: function () {
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
          email: this.email
        })
        console.log(datas)
        loginByEmail(datas).then(res => {
          this.mess = res.data.msg
          console.log(res.data)
          if (this.mess === 'User "' + this.account + '" login success') {
            this.$store.state.id = res.data.id
            this.$store.state.username = res.data.username
            this.$store.state.motto = res.data.motto
            this.$store.state.password = this.password
            this.$store.state.is_admin = res.data.is_admin
          }
        })
      }
    }
  }
}
</script>
