<template>
  <div id="home">
    <br>
    <h1>开始写markdown吧！</h1>
    <textarea type="text" name="mdtext" v-model=$store.state.mdtext></textarea>
    <h1></h1>
    <textarea type="text" name="mdtext" v-model=$store.state.mdtext readOnly = true></textarea>
    <h1></h1>
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
