<template>
  <v-layout row>
    <v-dialog
      persistent
      dark
      v-model="dataset.active"
      max-width="600"
    >
      <v-card>
        <v-card-title class="headline"> {{dataset.status}} </v-card-title>

        <v-card-text>
            <p :style="{display :  dataset.success ? 'block' : 'none'}">Time : {{dataset.time}} seconds.</p>
            <p :style="{display :  !dataset.success ? 'block' : 'none'}">Reason : {{dataset.reason}}</p>
            <p :style="{display :  dataset.type == 'R' ? 'block' : 'none'}">File Name : {{dataset.fname}}</p>
            <p :style="{display :  dataset.type == 'R' ? 'block' : 'none'}">Storage Path : {{dataset.path}}</p>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="lime darken-2"
            flat="flat"
            @click="dataset.active = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
  export default {
    props:['dataset'],
  }
</script>