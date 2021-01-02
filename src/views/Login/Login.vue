<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
    <el-button size='small' @click='print'>print</el-button>
    <el-form ref=for :model="form" label-width="80px" class="login-form">

        <el-form-item label="用户名" prop="username">
          <el-input v-model=username></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model=password type="password"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type=mess @click=login>登录</el-button>
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
      username: '',
      password: '',
      mess: ''
    }
  },
  computed: {
    canvertified: function () {
      return this.checkmess === 'Get verify code successfully'
    }
  },
  methods: {
    print: function () {
      console.log('debug information')
      console.log(this.$store.state.username)
      console.log(this.$store.state.id)
      console.log(this.$store.state.password)
      console.log(this.$store.state.motto)
    },
    login: function () {
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
