<template>
  <div id="notes">
    <h1>笔记列表</h1>
    <div v-if="noteCount">
      <table align="center">
        <thead>
          <tr>
            <th>课程</th>
            <th>文件名</th>
            <th>贡献者</th>
            <th>创建时间</th>
            <th>操作</th>
            <th>赞</th>
          </tr>
        </thead>
      <tbody>
        <tr v-for="item in noteList" :key="item" >
        <td>{{item.course}}</td>
        <td>{{item.name}}</td>
        <td>{{item.contributor}}</td>
        <td>{{item.date}}</td>
        <td><el-button v-on:click="download()" type="success" size = "small">下载</el-button></td>
        <td>{{item.upvote}} <el-button type="success" icon="el-icon-arrow-up" size = "small" @click="Upvote"></el-button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>笔记为空</h2>
    <h1></h1>
    <el-button v-on:click="addNote()" type="primary">添加笔记</el-button>
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
      this.$router.push('/home')
    },
    Upvote () {
    },
    Downvote () {
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
