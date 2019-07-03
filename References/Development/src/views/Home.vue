<template>
  <v-container fill-height>
    <v-layout align-center>
      <v-flex class="text-xs-center">
        <h1 class="deep-purple--text text--lighten-4 display-2">Welcome to Li-Fi GUI</h1>
        <br/>
        <router-link class="ablink" to="/load"><v-btn outline color="deep-purple lighten-3">Begin</v-btn></router-link>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    name: 'Home',
    components: {}
  }
</script>

<style scoped>
</style>
