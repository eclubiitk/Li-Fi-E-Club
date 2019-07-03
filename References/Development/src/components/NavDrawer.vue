<template>
  <v-layout>
    <v-toolbar dark fixed clipped-left app>
      <v-toolbar-title>Li-Fi Dashboard</v-toolbar-title>
      <About />
    </v-toolbar>
  </v-layout>
</template>

<script>
  import About from '../views/About'
  export default {
    name: "navdrawer",
    data () {
      return {
      }
    },
    components:{
      About
    }
  }
</script>

<style>
    .ablink{
        text-decoration-line: none
    }
</style>
