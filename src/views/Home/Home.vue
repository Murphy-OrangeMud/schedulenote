<template>
  <div id="home">
    <br>
    <h1>开始写markdown吧！</h1>
    <div class="note" style="position:relativel;margin-left:10%;margin-right:10%">
      <v-md-editor v-model="text" height="800px" ></v-md-editor><br>
      <el-button type="success" icon="el-icon-check" circle ></el-button>
      <el-button type="success" icon="el-icon-check" circle ></el-button>
    </div>
    <button v-on:click="savePDF()">保存pdf</button>
  </div>
</template>

<script>
export default {
  methods: {
    savePDF: function () {
    }
  }
}
</script>
