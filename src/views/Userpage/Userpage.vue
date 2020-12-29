<template>
    <div>
      <el-row :gutter="20" style="margin-top:10px;">
      <el-col :span="8" :offset="3">
      <div class="grid-content bg-purple">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>个人中心</span>
          </div>
          <div class="id">
            <span class="sender">id：{{data.id}}</span>
          </div>
          <div class="is_admin">
            <span class="sender">权限：{{showAuthority(data.is_admin)}}</span>
          </div>
          <div class="email">
            <span class="sender">邮箱：{{data.email}}</span>
          </div>
          <el-divider></el-divider>
          <div class="avatar">
            <span class="sender">头像：</span>
            <el-image
              style="width: 100px; height: 100px"
              :src="data.avatar"
              :fit="fit"></el-image>
          </div>
          <div class="username">
            <span class="sender">用户名：{{data.username}}</span>
          </div>
          <div class="password">
            <span class="sender">密码：{{data.password}}</span>
          </div>
          <div class="motto">
            <span class="sender">个性签名：{{data.motto}}</span>
          </div>
        </el-card>
    </div>
    </el-col>
    <el-col :span="10">
      <div class="grid-content bg-purple">
      <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>基本资料</span>
      </div>
      <div>
        <el-form label-width="80px" v-model="dataFrom" size="small" label-position="right">
          <el-form-item :label="头像" prop="avatar" ref="uploadElement">
          <el-upload ref="upload"
                     action="#"
                     accept="image/png,image/jpg,image/jpeg"
                     list-type="picture-card"
                     :limit=1
                     :auto-upload="false"
                     :on-exceed="handleExceed"
                     :before-upload="handleBeforeUpload"
                     :on-preview="handlePictureCardPreview"
                     :on-remove="handleRemove"
                     :on-change="imgChange"
                     :class="{hide:hideUpload}">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%"
                 :src="dialogImageUrl"
                 alt="">
          </el-dialog>
          </el-form-item>
          <el-form-item>
          <el-button size="small"
                     type="primary"
                     @click="uploadFile">立即上传</el-button>
          <el-button size="small"
          @click="tocancel">取消</el-button>
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input  auto-complete="off" v-model="formdata.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input auto-complete="off" v-model="formdata.password"></el-input>
          </el-form-item>
          <el-form-item label="个性签名" prop="motto">
            <el-input  maxlength="30" v-model="formdata.motto"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button size="mini" type="modify" @click=modify>提交</el-button>
        </div>
      </div>
      </el-card>
      </div>
    </el-col>
    </el-row>
    </div>
</template>

<script>
export default {
  data () {
    return {
      hideUpload: false,
      dialogImageUrl: '',
      dialogVisible: false,
      formLabelWidth: '80px',
      limitNum: 1,
      form: {},
      dialogVisible2: false,
      data: {
        id: 0,
        username: 'test',
        email: '1800012345@pku.edu.cn',
        password: '1234567',
        avatar: '',
        motto: '生活就像海洋，只有意志坚强的人才能到达彼岸',
        is_admin: false
      },
      formdata: {
        username: 'test',
        password: '1234567',
        avatar: '?',
        motto: '生活就像海洋，只有意志坚强的人才能到达彼岸'
      }
    }
  },
  methods: {
    showAuthority: function (isAdmin) {
      if (this.data.is_admin) return 'Admin'
      else return 'User'
    },
    modify: function () {
      this.data.username = this.formdata.username
      this.data.password = this.formdata.password
      this.data.avatar = this.formdata.avatar
      this.data.motto = this.formdata.motto
    },
    handleBeforeUpload (file) {
      if (!(file.type === 'image/png' || file.type === 'image/jpg' || file.type === 'image/jpeg')) {
        this.$notify.warning({
          title: '警告',
          message: '请上传格式为image/png, image/gif, image/jpg, image/jpeg的图片'
        })
      }
      var size = file.size / 1024 / 1024 / 2
      if (size > 4) {
        this.$notify.warning({
          title: '警告',
          message: '图片大小必须小于4M'
        })
      }
      var fd = new FormData()
      fd.append('picFile', file)
      console.log(fd.get('picFile'))
      this.api({
        url: '../../user_part/test_images',
        method: 'post',
        data: fd,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((data) => {

      })
    },
    // 文件超出个数限制时的钩子
    handleExceed (files, fileList) {

    },
    // 文件列表移除文件时的钩子
    handleRemove (file, fileList) {
      this.hideUpload = fileList.length >= this.limitNum
    },
    // 点击文件列表中已上传的文件时的钩子
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
    uploadFile () {
      this.$refs.upload.submit()
    },
    imgChange (files, fileList) {
      this.hideUpload = fileList.length >= this.limitNum
      if (fileList) {
        this.$refs.uploadElement.clearValidate()
      }
    },
    tocancel () {
      this.dialogVisible2 = false
    }
  }
}
</script>
