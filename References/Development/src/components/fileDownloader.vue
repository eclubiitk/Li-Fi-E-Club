<template>
  <v-layout row justify-center>
    <v-btn fab dark color="deep-orange darken-4" @click.stop="xval = true">
      <v-icon>cloud_download</v-icon>
    </v-btn>
    <v-dialog v-model="xval" persistent dark max-width="600">
      <v-card dark>
        <v-card-title>
          <span class="headline">Reception Panel</span>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-2" flat @click="xval = false">Cancel</v-btn>
          <v-btn color="red darken-2" flat @click="beginTransfer">Begin Reception</v-btn>
          <loader :dispdata="loadstat.title" :dialog="loadstat.stat" :color="loadstat.color"/>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <transferStatus :dataset="responseval"/>
  </v-layout>
</template>

<script>
  import axios from "axios";
  import loader from './loader';
  import transferStatus from './transferStatus'
  export default {
    name: 'fileUploader',
    data () {
      return {
        xval: false,
        file:'',
        loadstat:{
          'title':"Reception in Progress",
          'stat':false,
          'color':'deep-orange darken-4'
        },
        responseval:{
          active:false,
          status:"",
          success:false,
          reason:""
        }
      }
    },

    components : {
      loader,
      transferStatus
    },

    methods : {
      handleFileUpload(){
        this.file = this.$refs.file.files[0]
      },
      beginTransfer(){
        this.xval=false
        this.loadstat.stat=true
        let ldst=this.loadstat
        let responseval=this.responseval
        let formData = new FormData();
        formData.append('filetoupload', this.file);
        axios.post( 'http://localhost:30000/receive',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(function(response) {
          ldst.stat=false
          responseval=response.data
          responseval.active=true
          }).catch(function(){
          ldst.stat=false
          responseval.status="Reception Failed"
          responseval.active=true
          responseval.success=false
          responseval.reason="Either the Server is closed or File received is damaged."
          responseval.type='R!'
          });
      }
    }
  }
</script>