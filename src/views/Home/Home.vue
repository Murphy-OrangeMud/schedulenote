<template>
  <div id="home">
    <br>
    <h1>开始写markdown吧！</h1>
    <div class="note" style="position:relative;margin-left:10%;margin-right:10%">
      <v-md-editor v-model="text" height="800px" ></v-md-editor><br>
      <el-button type="success" icon="el-icon-caret-top" round style="position:relative;margin-left:36%;">赞</el-button>
      <el-button type="success" icon="el-icon-caret-bottom" round style="position:relative;">踩</el-button>
      <el-button type="primary" plain style="position:relative;margin-left:46%"
      @click="savePDF()">保存pdf</el-button>
    </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      text: 'Hello'
    }
  },
  methods: {
    savePDF: function () {
    }
  }
}
</script>
