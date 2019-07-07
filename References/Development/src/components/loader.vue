<template>
  <div class="text-xs-center">
    <v-dialog
      v-model="dialog"
      persistent
      width="300"
    >
      <v-card
        :color="color"
        dark
      >
        <v-card-text>
          {{dispdata}}
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    props: ['dispdata', 'dialog', 'color'],
  }
</script>