<template>
  <div id="notes">
    <h1>课程资料列表</h1>
    <div v-if="MaterialList.length">
      <table align="center">
        <thead>
          <tr>
            <th>课程</th>
            <th>文件名</th>
            <th>贡献者</th>
            <th>操作</th>
            <th>赞</th>
          </tr>
        </thead>
      <tbody>
        <tr v-for="item in MaterialList" :key="item" >
        <td>{{item.coursename}}</td>
        <td>{{item.filename}}</td>
        <td>{{item.uploader}}</td>
        <td><button v-on:click="download()">下载</button></td>
        <td>{{item.score}} <el-button type="success" icon="el-icon-arrow-up" size = "small" @click="Upvote"></el-button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>课程资料为空</h2>
    <h1></h1>
    <button v-on:click="addMaterials()">添加资料</button>
  </div>
</template>

<script>
import { getHomeMultidata } from 'network/home'
export default {
  name: 'notes',
  data () {
    return {
      MaterialList: []
    }
  },
  computed: {
  },
  methods: {
    download () {
    },
    addMaterials () {
    },
    Upvote () {
    },
    Downvote () {
    },
    getHomeMultidata () {
      getHomeMultidata().then(res => {
        this.MaterialList = res.MaterialList
      })
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
