<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
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
    login: function () {
      const datas = qs.stringify({
        name: this.username,
        password: this.password
      })
      console.log(datas)
      event.preventDefault()
      postLogin(datas).then(res => {
        this.mess = res.data.msg
        console.log(res)
        if (this.mess === 'User "' + this.username + '" login success') {
          this.$store.state.id = res.data.id
          this.$store.state.username = res.data.username
          this.$store.state.motto = res.data.motto
          this.$store.state.password = this.password
          this.$store.state.is_admin = res.data.is_admin
          this.$router.push('/Userpage')
        }
      })
    }
  }
}
</script>
