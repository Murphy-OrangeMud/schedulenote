<template>
  <div id="login">
    <h1>Schedule note 用户注册</h1>
    <el-form ref=for label-width="80px" class="login-form">

        <el-form-item label="用户名" prop="username">
          <el-input v-model=username></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model=password type="password"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type=mess @click=regis>注册</el-button>
        </el-form-item>
      </el-form>
      <div v-if=mess>
        <el-tag type="success">{{mess}}</el-tag>
      </div>
  </div>
</template>

<script>
import { postRegister } from 'network/home'
import qs from 'qs'
export default {
  name: 'register',
  data () {
    return {
      username: '',
      password: '',
      mess: '',
      email: ''
    }
  },
  methods: {
    regis: function () {
      this.email = ''
      const leng = Math.round(Math.random() * 40) + 20
      let i = 0
      for (i = 0; i < leng; ++i) {
        this.email += Math.round(Math.random() * 9)
      }
      const datas = qs.stringify({
        name: this.username,
        password: this.password,
        email: this.email
      })
      console.log(datas)
      postRegister(datas).then(res => {
        this.mess = res.data.msg
      })
    }
  }
}
</script>
