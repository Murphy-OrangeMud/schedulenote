<template>
  <div id="home">
    <br>
    <h1>开始写markdown吧！</h1>
    <div class="note" style="position:relative;margin-left:10%;margin-right:10%">
      <v-md-editor v-model="text" id = "printMe" height="800px" ></v-md-editor><br>
      <el-button type="primary" plain style="position:relative;margin-left:46%"
      v-print="printObj">保存pdf</el-button>
    </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      text: 'Hello',
      printObj: {
        id: 'printMe',
        popTitle: 'good print',
        extraCss: 'https://www.google.com,https://www.google.com',
        extraHead: '<meta http-equiv="Content-Language"content="zh-cn"/>'
      }
    }
  },
  methods: {
  }
}
</script>
