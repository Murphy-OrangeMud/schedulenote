<template>
  <div id="notes">
    <h1>Note列表</h1>
    <div v-if="noteCount">
      <table align="center">
        <thead>
          <tr>
            <th>课程</th>
            <th>文件名</th>
            <th>贡献者</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
      <tbody>
        <tr v-for="item in noteList" :key="item" >
        <td>{{item.course}}</td>
        <td>{{item.name}}</td>
        <td>{{item.contributor}}</td>
        <td>{{item.date}}</td>
        <td><button v-on:click="download()">下载</button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>ddl为空</h2>
    <h1></h1>
    <button v-on:click="addNote()">添加note</button>
  </div>
</template>

<script>
export default {
  name: 'notes',
  computed: {
    noteList () {
      return this.$store.state.noteList
    },
    noteCount () {
      return this.$store.state.noteList.length
    }
  },
  methods: {
    download () {
    },
    addNote () {
    }
  }
}
</script>

<style>
table {
  border: 1px solid #e9e9e9;
  border-collapse: collapse;
  border-spacing: 0;
}

th, td {
  padding: 8px 16px;
  border: 1px solid #e9e9e9;
  text-align: left;
}

th {
  background-color: #f7f7f7;
  color: #5c6b77;
  font-weight: 600;
}
</style>
