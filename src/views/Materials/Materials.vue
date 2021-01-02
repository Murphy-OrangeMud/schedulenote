<template>
  <div id="notes">
    <h1>课程资料列表</h1>
    <div v-if="materialList.length">
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
        <tr v-for="item in materialList" :key="item" >
        <td>{{item.coursename}}</td>
        <td>{{item.filename}}</td>
        <td>{{item.uploader}}</td>
        <td>{{item.date}}</td>
        <td><el-button v-on:click="download(item, item.fileid)" size="small" type="success">下载</el-button></td>
        <td>{{item.score}} <el-button type="success" icon="el-icon-arrow-up" size = "small" @click="Upvote(item, item.fileid)"></el-button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>课程资料为空</h2>
    <h1></h1>
    附件名称：<el-input v-model="addFileName" autocomplete="off" size="small" style="width: 300px;" ></el-input>
    <div class="add-file-right" style="height:70px;margin-top:15px;">
        <div class="add-file-right-img">上传文件：</div>
        <input type="file" ref="clearFile" @change="getFile($event)" multiple="multiplt" class="add-file-right-input" style="margin-left:70px;" accept=".docx,.doc,.pdf,.md">
        <span class="add-file-right-more">支持扩展名：.doc .docx .pdf .md </span>
    </div>
    <div class="add-file-list">
        <ul>
            <li v-for="(item, index) in addArr" :key="index"><a >{{item.name}}</a></li>
        </ul>
    </div>
    <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitAddFile" size="small">开始上传</el-button>
        <el-button @click="resetAdd" size="small">全部删除</el-button>
    </div>
  </div>
</template>

<script>
import { getFilelist, postFilelist, postMaterials, getMaterials } from 'network/home'
export default {
  name: 'materials',
  data () {
    return {
      materialList: [],
      addArr: [],
      mess: '',
      ge: []
    }
  },
  computed: {
    MaterialList () {
      return this.materialList
    },
    MaterialCount () {
      return this.materialList.length
    }
  },
  methods: {
    download (item, ID) {
      var formData = new FormData()
      formData.append('id', ID)
      getMaterials(formData).then(res => {
        console.log(res)
        console.log(item.filename)
        const blob = new Blob([res])
        console.log(blob)
        const urlObject = window.URL || window.webkitURL || window
        const link = document.createElement('a')
        link.href = urlObject.createObjectURL(blob)
        link.download = item.filename
        link.click()
        console.log(res)
        console.log(link)
        window.URL.revokeObjectURL(link.href)
      })
    },
    addMaterials () {
    },
    myGetFilelist () {
      var formData = new FormData()
      formData.append('id', this.$store.state.courseid)
      getFilelist(formData).then(res => {
        this.materialList = res
      })
    },
    Upvote (item, id) {
      postFilelist({ id })
      this.myGetFilelist()
    },
    getFile (event) {
      var file = event.target.files
      for (var i = 0; i < file.length; i++) {
        this.addArr.push(file[i])
      }
    },
    submitAddFile () {
      for (var i = 0; i < this.addArr.length; i++) {
        if (this.addArr.length === 0) {
          this.$message(
            {
              type: 'info',
              message: '请选择要上传的文件'
            }
          )
          return
        }
        var formData = new FormData()
        formData.append('course', 2)
        formData.append('uploader', 2)
        formData.append('description', 'hzj')
        formData.append('file', this.addArr[i])

        postMaterials(formData).then(res => {
          if (res.data.code === 200) {
            this.$message({
              type: 'success',
              message: '附件上传成功!'
            })
          }
          if (res.data.code === 400) {
            this.$message({
              type: 'fail',
              message: '已有同名文件!'
            })
          }
        })
        this.myGetFilelist()
      }
    },
    resetAdd () {
      this.addArr = []
    }
  },
  created () {
    this.myGetFilelist()
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
