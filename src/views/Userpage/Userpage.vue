<template>
  <div>
    <el-button size='small' @click='print'>print</el-button>
    <el-row :gutter='20' style='margin-top: 10px'>
      <el-col :span='8' :offset='3'>
        <div class='grid-content bg-purple'>
          <el-card class='box-card'>
            <div slot='header' class='clearfix'>
              <span>个人中心</span>
            </div>
            <div class='id'>
              <span class='sender'>id：{{ id }}</span>
            </div>
            <div class='is_admin'>
              <span class='sender'>权限：{{ showAuthority(is_admin) }}</span>
            </div>
            <div class='email'>
              <span class='sender'>邮箱：{{ email }}</span>
            </div>
            <el-divider></el-divider>
            <div class='avatar'>
              <span class='sender'>头像：</span>
              <el-image
                style='width: 100px; height: 100px'
                :src='avatar'
                :fit='fit'
              ></el-image>
            </div>
            <div class='username'>
              <span class='sender'>用户名：{{ username }}</span>
            </div>
            <div class='password'>
              <span class='sender'>密码：{{ password }}</span>
            </div>
            <div class='motto'>
              <span class='sender'>个性签名：{{ motto }}</span>
            </div>
          </el-card>
        </div>
      </el-col>
      <el-col :span='10'>
        <div class='grid-content bg-purple'>
          <el-card class='box-card'>
            <div slot='header' class='clearfix'>
              <span>基本资料</span>
            </div>
            <div>
              <el-form
                label-width='80px'
                v-model='dataFrom'
                size='small'
                label-position='right'
              >
                <el-form-item :label='头像' prop='avatar' ref='uploadElement'>
                  <el-upload
                    ref='upload'
                    action='#'
                    accept='image/png,image/jpg,image/jpeg'
                    list-type='picture-card'
                    :limit='1'
                    :auto-upload='false'
                    :on-exceed='handleExceed'
                    :before-upload='handleBeforeUpload'
                    :on-preview='handlePictureCardPreview'
                    :on-remove='handleRemove'
                    :on-change='imgChange'
                    :class='{ hide: hideUpload }'
                  >
                    <i class='el-icon-plus'></i>
                  </el-upload>
                  <el-dialog :visible.sync='dialogVisible'>
                    <img width='100%' :src='dialogImageUrl' alt='' />
                  </el-dialog>
                </el-form-item>
                <el-form-item>
                  <el-button size='small' type='primary' @click='uploadFile'
                    >立即上传</el-button
                  >
                  <el-button size='small' @click='tocancel'>取消</el-button>
                </el-form-item>
                <el-form-item label='用户名' prop='username'>
                  <el-input
                    auto-complete='off'
                    v-model='formdata.username'
                  ></el-input>
                </el-form-item>
                <el-form-item label='密码' prop='password'>
                  <el-input
                    auto-complete='off'
                    v-model='formdata.password'
                  ></el-input>
                </el-form-item>
                <el-form-item label='个性签名' prop='motto'>
                  <el-input maxlength='30' v-model='formdata.motto'></el-input>
                </el-form-item>
              </el-form>
              <div slot='footer' class='dialog-footer'>
                <el-button size='mini' type='modify' @click='modify'
                  >提交</el-button
                >
                <el-button size='mini' type='modify' @click='logout'
                  >登出</el-button
                >
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
      <div v-if='not_login'>请先登录!</div>
    </el-row>
  </div>
</template>

<script>
import { postLogout, addavatar } from 'network/home'
export default {
  // eslint-disable-next-line space-before-function-paren
  data() {
    return {
      hideUpload: false,
      dialogImageUrl: '',
      dialogVisible: false,
      formLabelWidth: '80px',
      limitNum: 1,
      form: {},
      files: null,
      imageUrl: null,
      dialogVisible2: false,
      data: {},
      formdata: {
        username: 'alice',
        password: '123',
        avatar: '',
        motto: ''
      }
    }
  },
  computed: {
    id () {
      return this.$store.state.id
    },
    username () {
      return this.$store.state.username
    },
    email () {
      return this.$store.state.email
    },
    avatar () {
      return this.$store.state.avatar
    },
    motto () {
      return this.$store.state.motto
    },
    is_admin () {
      return this.$store.state.is_admin
    },
    password () {
      return this.$store.state.password
    },
    not_login () {
      return this.$store.state.username === ''
    }
  },
  methods: {
    print: function () {
      console.log(this.$store.state.username)
      console.log(this.$store.state.id)
      console.log(this.$store.state.password)
    },
    showAuthority: function (isAdmin) {
      if (this.data.is_admin) return 'Admin'
      else return 'User'
    },
    addAvatar: function () {
      const datas = {
        avatar: this.formdata.avatar
      }
      if (
        !(
          datas.avatar.type === 'image/png' ||
          datas.avatar.type.type === 'image/jpg' ||
          datas.avatar.type.type === 'image/jpeg'
        )
      ) {
        console.log('不是图片')
      }
      addavatar(datas)
    },
    modify: function () {
      clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        console.log('modify modify modify modify modify modify modify ')
        console.log(this.$store.state)
        this.$store.state.username = this.formdata.username
        this.$store.state.password = this.formdata.password
        this.$options.methods.addAvatar()
        //  this.$store.state.avatar = 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
        this.$store.state.motto = this.formdata.motto
        console.log('ok')
      }, 3000)
    },
    logout: function () {
      postLogout().then((res) => {
        console.log('logout logout logout logout logout')
        console.log(this.$store.state)
        if (this.mess === 'Logout Success') {
          alert('登出成功！')
          this.$store.state.id = 0
          this.$store.state.username = ''
          this.$store.state.motto = ''
          this.$store.state.password = ''
          this.$store.state.is_admin = false
          this.$store.state.avatar = ''
        }
      })
    },
    handleBeforeUpload (file) {
      if (
        !(
          file.type === 'image/png' ||
          file.type === 'image/jpg' ||
          file.type === 'image/jpeg'
        )
      ) {
        this.$notify.warning({
          title: '警告',
          message:
            '请上传格式为image/png, image/gif, image/jpg, image/jpeg的图片'
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
    },
    // 文件超出个数限制时的钩子
    handleExceed (files, fileList) {},
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
      const datas = {
        avatar: this.files.url
      }
      console.log(datas)
      addavatar(datas).then(res => {
        if (res.data.code === '200') {
          this.avatar = this.imageUrl
        }
      })
    },
    imgChange (files, fileList) {
      // this.hideUpload = fileList.length >= this.limitNum
      // if (fileList) {
      //   this.$refs.uploadElement.clearValidate()
      // }
      this.files = files
      this.imageUrl = files.url
    },
    tocancel () {
      this.dialogVisible2 = false
    },
    onUpload () {
      var file = this.files[0]
      /* eslint-disable no-undef */
      const param = new FormData() // 创建form对象
      param.append('avatar', file) // 通过append向form对象添加数据
      param.append('chunk', '0') // 添加form表单中其他数据
      console.log(param.get('file')) // FormData私有类对象，访问不到，可以通过get判断值是否传进去
      const config = {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
      // 添加请求头
      this.axios
        .post('http://8.136.141.151:8848/user/upload_avatar', param, config)
        .then((res) => {
          console.log(res)
        })
    }
  }
}
</script>
