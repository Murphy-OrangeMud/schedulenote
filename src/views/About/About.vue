<template>
  <div id="about">
    <h1>About</h1>
    <p>这是一个笔记分享软件，可以在线转换markdown。</p>
    <el-button size='small' @click='print'>print</el-button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: {}
    }
  },
  methods: {
    print: function () {
      console.log('debug information')
      console.log(this.$store.state.username)
      console.log(this.$store.state.id)
      console.log(this.$store.state.password)
      console.log(this.$store.state.motto)
    }
  }
}
</script>
