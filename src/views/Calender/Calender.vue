<template>
  <div id = "calendar">
    <full-calendar :events="fcEvents"
    @changeMonth="changeMonth"
    @eventClick="eventClick"
    @dayClick="dayClick"
    @moreClick="moreClick"></full-calendar>
    <button v-on:click="refresh()">刷新</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      fcEvents: this.$store.state.ddlList
    }
  },
  components: {
    'full-calendar': require('vue-fullcalendar')
  },
  methods: {
    changeMonth () {
    },
    eventClick (event) {
      if (confirm('是否要删除' + event.title + '？')) {
        console.log('delete')
      }
    },
    dayClick (day, jsEvent) {
      if (confirm('是否要在' + day + '添加一个DDL？')) {
        console.log('add')
      }
    },
    moreClick () {
    },
    refresh () {
      console.log('刷新')
    }
  }
}
</script>

<!--
<template>
  <div id="calender">
    <h1>日历界面</h1>
    <div v-if="ddlCount">
      <table align="center">
        <thead>
          <tr>
            <th>日期</th>
            <th>课程</th>
            <th>任务</th>
            <th>操作</th>
          </tr>
        </thead>
      <tbody>
        <tr v-for="item in ddlList" :key="item" >
        <td>{{item.date}}</td>
        <td>{{item.course}}</td>
        <td>{{item.task}}</td>
        <td><button v-on:click="deleteDdl()">移除</button></td>
        </tr>
      </tbody>
      </table>
    </div>
    <h2 v-else>ddl为空</h2>
    <h1></h1>
    <button v-on:click="addDdl()">添加事件</button>
    <button v-on:click="refresh()">刷新</button>
  </div>
</template>

<script>
export default {
  name: 'calender',
  computed: {
    ddlList () {
      return this.$store.state.ddlList
    },
    ddlCount () {
      return this.$store.state.ddlList.length
    }
  },
  methods: {
    deleteDdl () {
    },
    addDdl () {
      // skipher
    },
    refresh: function () {
      this.$axios.defaults.baseURL = 'http://localhost:8080/api'
      this.$axios.get('/api/getDDL')
        .then((response) => {
          console.log(response)
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
-->
