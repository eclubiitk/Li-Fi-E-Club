<template>
  <v-layout row justify-center>
    <v-btn fab dark color="green darken-4" @click.stop="xval = true">
      <v-icon>cloud_upload</v-icon>
    </v-btn>
    <v-dialog v-model="xval" persistent dark max-width="600">
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
          <v-btn color="green darken-1" flat @click="xval = false">Cancel</v-btn>
          <v-btn color="green darken-1" flat @click="beginTransfer">Begin Transmission</v-btn>
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
          'title':"Transmission in Progress",
          'stat':false,
          'color':'green darken-4'
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
        axios.post( 'http://localhost:30000/transmit',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(function(response) {
          ldst.stat=false
          responseval.active=true
          responseval.success=true
          responseval.status=response.data.status
          responseval.time=response.data.time
          responseval.speed=response.data.speed
          responseval.type='T'
          }).catch(function(){
          ldst.stat=false
          responseval.status="Transmission Failed"
          responseval.active=true
          responseval.success=false
          responseval.reason="Either the Server is closed or File sent is damaged."
          responseval.type='T!'
          });
      }
    }
  }
</script>