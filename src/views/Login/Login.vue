<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
    <el-form ref="form" :rules="rules" :model="form" label-width="80px" class="login-form">

        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password"></el-input>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('form')">登录</el-button>
        </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default {
  data () {
    const validateNumber = (rule, value, callback) => {
      if (!value) {
        callback(new Error('用户名不能为空'))
      } else {
        callback()
      }
    }
    return {
      form: {
        username: '',
        password: '',
        email: ''
      },
      rules: {
        username: [
          { type: 'number', validator: validateNumber }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 7, max: 15, message: '密码7-15位', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('注册成功!')
          this.$router.push('/home')
        } else {
          alert('注册失败!请正确填写注册信息!')
          return false
        }
      })
    }
  }
}

</script>
