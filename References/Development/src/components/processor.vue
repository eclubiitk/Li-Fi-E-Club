<template>
  <v-card id="create">
    <v-speed-dial
      v-model="fab"
      :direction="direction"
      :open-on-hover="hover"
      :transition="transition"
    >
      <template v-slot:activator>
        <v-btn v-model="fab" color="blue darken-2" dark fab>
          <v-icon>import_export</v-icon>
          <v-icon>close</v-icon>
        </v-btn>
      </template>
      <fileUploader />
      <v-btn fab dark small color="red" @click="startReception">
        <v-icon>cloud_download</v-icon>
      </v-btn>
    </v-speed-dial>
  </v-card>
</template>

<script>
  import axios from 'axios'
  import fileUploader from './fileUploader'
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
      fileUploader
    },

    methods: {
      startReception() {
        axios.post('http://localhost:30000/receive',{}).then(function(response){alert("Transmission Successful")}).catch(function(){alert('Either the file is damaged or Server is not running.');});
      }
    },

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