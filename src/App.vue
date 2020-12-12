<template>
  <div id="app">
<<<<<<< Updated upstream
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/test">Test</router-link>
    </div>
=======
    <router-link to="/register">Register</router-link> |
    <router-link to="/login">Login</router-link> |
    <router-link to="/home">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/calender">Calender</router-link> |
    <router-link to="/notes">Notes</router-link>
>>>>>>> Stashed changes
    <router-view />
  </div>
</template>

<style>
@import "assets/css/normalize.css";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #99ffff;
}

</style>

<script>

export default {
  name: 'app'
}
</script>
