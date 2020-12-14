<template>
  <div id="notes">
    <h1>课程资料列表</h1>
    <div v-if="MaterialCount">
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
        <tr v-for="item in MaterialList" :key="item" >
        <td>{{item.coursename}}</td>
        <td>{{item.filename}}</td>
        <td>{{item.uploader}}</td>
        <td>{{item.date}}</td>
        <td><button v-on:click="download()">下载</button></td>
        <td>{{item.score}} <el-button type="success" icon="el-icon-arrow-up" size = "small" @click="Upvote(item, item.fileid)"></el-button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>课程资料为空</h2>
    <h1></h1>
    <button v-on:click="addMaterials()">上传资料</button>
  </div>
</template>

<script>
import { getHomeMultidata, postHomeMultidata } from 'network/home'
export default {
  name: 'notes',
  computed: {
    MaterialList () {
      return this.$store.state.materialList
    },
    MaterialCount () {
      return this.$store.state.materialList.length
    }
  },
  methods: {
    download () {
    },
    addMaterials () {
    },
    Upvote (item, id) {
      item.score += 1
      postHomeMultidata({ id })
    },
    Downvote () {
    },
    getHomeMultidata () {
      getHomeMultidata().then(res => {
        this.MaterialList = res
      })
    }
  },
  created () {
    this.getHomeMultidata()
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
