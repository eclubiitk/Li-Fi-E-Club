<template>
  <v-app id="back">
    <v-content>
      <navdrawer/>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import navdrawer from './components/NavDrawer'

export default {
  name: 'App',
  components: {
    navdrawer
  },
  data () {
    return {
      //
    }
  }
}
</script>

<style scoped>
  #back {
    background-image: url(https://images.wallpaperscraft.com/image/light_abstract_dark_space_88100_1920x1080.jpg);
    background-size: cover;
  }
</style>

