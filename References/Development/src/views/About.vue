<template>
  <v-layout justify-end>
    <v-icon @click.stop="dialog = true">help</v-icon>

    <v-dialog dark v-model="dialog" max-width="400" >
      <v-card>
        <v-card-title class="headline">About Li-Fi : GUI</v-card-title>

        <v-card-text>
          This is the Graphical User Interface for Li-Fi created by Utkarsh Gupta.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="blue lighten-2"
            flat="flat"
            @click="dialog = false"
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
    name: 'About',
    data () {
      return {
        dialog: false
      }
    }
  }
</script>