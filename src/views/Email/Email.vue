<template>
  <div id="email">
    <el-input v-model="input" placeholder="请输入邮箱中收到的的验证码"></el-input>
    <el-button type="primary">提交</el-button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      input: ''
    }
  }
}
</script>
