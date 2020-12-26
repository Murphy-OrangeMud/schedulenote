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
          <div class="username">
            <span class="sender">用户名：{{data.username}}</span>
          </div>
          <div class="password">
            <span class="sender">密码：{{data.password}}</span>
          </div>
          <div class="avatar">
            <span class="sender">头像：{{data.avatar}}</span>
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
          <el-form-item label="用户名" prop="username">
            <el-input  auto-complete="off" v-model="formdata.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input auto-complete="off" v-model="formdata.password"></el-input>
          </el-form-item>
          <el-form-item label="头像" prop="avatar">
            <el-input auto-complete="off" v-model="formdata.avatar"></el-input>
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
      data: {
        id: 0,
        username: 'test',
        email: '1800012345@pku.edu.cn',
        password: '1234567',
        avatar: '?',
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
    }
  }
}
</script>
