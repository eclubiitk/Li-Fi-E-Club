<template>
  <v-card id="create">
    <v-speed-dial
      v-model="fab"
      :direction="direction"
      :open-on-hover="hover"
      :transition="transition"
    >
      <template v-slot:activator>
        <v-btn v-model="fab" color="deep-purple darken-4" large dark fab>
          <v-icon>import_export</v-icon>
          <v-icon>close</v-icon>
        </v-btn>
      </template>
      <fileUploader />
      <fileDownloader />
    </v-speed-dial>
  </v-card>
</template>

<script>
  import fileUploader from './fileUploader'
  import fileDownloader from './fileDownloader'
  export default {
    data: () => ({
      direction: 'right',
      fab: false,
      fling: false,
      hover: false,
      tabs: null,
      transition: 'scale-transition'
    }),

    components: {
      fileUploader,
      fileDownloader
    },

    methods: {},

    computed: {
      activeFab () {
        switch (this.tabs) {
          case 'one': return { 'class': 'purple', icon: 'account_circle' }
          case 'two': return { 'class': 'red', icon: 'edit' }
          case 'three': return { 'class': 'green', icon: 'keyboard_arrow_up' }
          default: return {}
        }
      }
    }
  }
</script>

<style scoped>
  #create .v-speed-dial {
    position: absolute;
  }
  #create .v-btn--floating {
    position: relative;
  }
</style>