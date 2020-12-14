<template>
  <div id="login">
    <h1>Schedule note 用户登录</h1>
    <el-form ref="form" :rules="rules" :model="form" label-width="80px" class="login-form">

        <el-form-item label="学工号" prop="username">
          <el-input v-model.number="form.username"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password"></el-input>
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
      console.log(typeof (value))
      console.log(value > 1)
      if (!value) {
        callback(new Error('学工号不能为空'))
      } else if (typeof (value) !== 'number') {
        callback(new Error('学工号应该是数字'))
      } else if (value < 1000000000 || value > 9999999999) {
        callback(new Error('请输入10位数学工号'))
      } else {
        callback()
      }
    }
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { type: 'number', validator: validateNumber }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 7, max: 15, message: '密码7-15位', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    register: function () {
      this.$router.push('/register')
    },
    loginCheck: function () {
      this.$router.push('/home')
    }
  }
}

</script>
