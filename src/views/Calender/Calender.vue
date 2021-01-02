<template>
  <div id="calender">
    <full-calendar :events="ddlList" class="test-fc" first-day='1' locate="fr"
    @eventClick="eventClick">
    </full-calendar>
    <h1></h1>
    <el-form ref=for label-width="80px" class="login-form">

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
  data () {
    return {
      ddlList: [],
      resddl: [],
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
  components: {
    'full-calendar': require('vue-fullcalendar')
  },
  methods: {
    getDdl () {
      const datas = { userID: this.$store.state.id + '' }
      console.log(datas)
      getddl(datas).then(res => {
        console.log(res)
        this.ddlList = []
        let i = 0
        for (i = 0; i < res.calendar.length; i += 1) {
          this.ddlList.push({
            title: res.calendar[i].description,
            start: res.calendar[i].startTime.split(' ')[0],
            end: res.calendar[i].endTime.split(' ')[0],
            YOUR_DATA: {
              id: res.calendar[i].id
            }
          })
        }
        this.resddl = res.calendar
        this.mess = '成功获取ddl'
        console.log(this.resddl)
        console.log(this.ddlList)
      })
    },
    eventClick (event, jsEvent, pos) {
      console.log('eventClick')
      if (confirm('是否要删除' + event.title + '？')) {
        const datas = {
          id: event.YOUR_DATA.id
        }
        console.log(datas)
        delddl(datas).then(res => {
          this.mess = '删除ddl成功'
        })
        this.getDdl()
      }
    },
    addDdl () {
      const datas = {
        description: this.myddl.description,
        startTime: this.myddl.startTime1 + ' ' + this.myddl.startTime2 + ':00',
        endTime: this.myddl.endTime1 + ' ' + this.myddl.endTime2 + ':00',
        location: this.myddl.location,
        rotation: 100,
        userID: this.$store.state.id + '',
        type: 2
      }
      console.log(datas)
      this.mess = '未能添加ddl'
      addddl(datas).then(res => {
        this.mess = '添加ddl成功'
        console.log(res)
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
