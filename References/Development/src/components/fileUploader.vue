<template>
  <v-layout row justify-center>
    <v-btn fab dark small color="green">
      <v-icon @click.stop="xval = true">cloud_upload</v-icon>
    </v-btn>
    <v-dialog v-model="xval" persistent max-width="600">
      <v-card dark>
        <v-card-title>
          <span class="headline">Transmission Panel</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex>
                <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="xval = false">Cancel</v-btn>
          <v-btn color="blue darken-1" flat @click="beginTransfer">Begin Transmission</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
  import axios from "axios";
  export default {
    name: 'fileUploader',
    data () {
      return {
        xval: false,
        file:''
      }
    },

    methods : {
      handleFileUpload(){
        this.file = this.$refs.file.files[0]
      },
      beginTransfer(){
        let formData = new FormData();
        formData.append('filetoupload', this.file);
        axios.post( 'http://localhost:30000/transmit',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(function(response){alert("Transmission Successful")}).catch(function(){alert('Either the file is damaged or Server is not running.');});
      }
    }
  }
</script>