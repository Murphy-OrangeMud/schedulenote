<template>
  <div id="calender">
    <h1>日历界面</h1>
    <div v-if="ddlList.length">
      <table align="center">
        <thead>
          <tr>
            <th>描述</th>
            <th>开始时间</th>
            <th>结束时间</th>
            <th>地点</th>
            <th>操作</th>
          </tr>
        </thead>
      <tbody>
        <tr v-for="item in ddlList" :key="item" >
        <td>{{item.description}}</td>
        <td>{{item.startTime}}</td>
        <td>{{item.endTime}}</td>
        <td>{{item.location}}</td>
        <td><el-button v-on:click="delDdl(item.id)" type="danger" size="small">移除</el-button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>ddl为空</h2>
    <h1></h1>
    <el-form ref=for :model="form" label-width="80px" class="login-form">

        <el-form-item label="描述" prop="username">
          <el-input v-model="myddl.description"></el-input>
        </el-form-item>

        <el-form-item label="开始时间">
            <el-col :span="11">
              <el-input type="date" placeholder="选择日期" v-model=myddl.startTime1 style="width: 100%;"></el-input>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-input type="time" placeholder="选择时间" v-model=myddl.startTime2 style="width: 100%;"></el-input>
            </el-col>
          </el-form-item>

          <el-form-item label="结束时间">
              <el-col :span="11">
                <el-input type="date" placeholder="选择日期" v-model=myddl.endTime1 style="width: 100%;"></el-input>
              </el-col>
              <el-col class="line" :span="2">-</el-col>
              <el-col :span="11">
                <el-input type="time" placeholder="选择时间" v-model=myddl.endTime2 style="width: 100%;"></el-input>
              </el-col>
            </el-form-item>

        <el-form-item label="地点" prop="password">
          <el-input v-model="myddl.location"></el-input>
        </el-form-item>
      </el-form>
    <el-button v-on:click="addDdl()" type="primary">添加事件</el-button>
    <el-button v-on:click="refresh()" type="primary">刷新</el-button>
    <div v-if=mess>
      <el-tag type="success">{{mess}}</el-tag>
    </div>
  </div>
</template>

<script>

import { getddl, addddl, delddl } from 'network/home'
export default {
  name: 'calender',
  data () { // asdf
    return {
      ddlList: [],
      myddl: {
        description: '',
        startTime1: '',
        startTime2: '',
        endTime1: '',
        endTime2: '',
        location: ''
      },
      mess: '未能获取ddl'
    }
  },
  methods: {
    getDdl () {
      const datas = { userID: '100' }
      console.log(datas)
      getddl(datas).then(res => {
        this.ddlList = res.calendar
        this.mess = '成功获取ddl'
      })
    },
    delDdl (id) {
      const datas = {
        id: id
      }
      this.mess = '未能删除ddl'
      delddl(datas).then(res => {
        this.mess = '删除ddl成功'
      })
      this.getDdl()
    },
    addDdl () {
      const datas = {
        description: this.myddl.description,
        startTime: this.myddl.startTime1 + ' ' + this.myddl.startTime2,
        endTime: this.myddl.endTime1 + ' ' + this.myddl.endTime2,
        location: this.myddl.location,
        rotation: 100,
        userID: '100',
        type: 2
      }
      console.log(datas)
      this.mess = '未能添加ddl'
      addddl(datas).then(res => {
        this.mess = '添加ddl成功'
      })
      this.getDdl()
    },
    refresh: function () {
      this.getDdl()
    }
  },
  created () {
    this.getDdl()
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
