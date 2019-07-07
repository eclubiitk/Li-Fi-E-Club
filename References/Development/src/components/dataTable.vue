<template>
  <div style="padding-top:5%">
    <div style="text-align:center">
    </div>
    <v-toolbar flat dark>
      <v-toolbar-title>Device Data</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn dark color="brown darken-3" @click="updatePortinfo()" style="float:right">Update Configuration</v-btn>
      <v-dialog v-model="dialog" dark max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm6 md6>
                    <br/>
                  <p label="Name">{{ editedItem.name }}</p>
                </v-flex>
                <v-flex xs12 sm6 md6>
                  <v-overflow-btn editable :items="availPort" label="Select port" v-model="editedItem.value" outline></v-overflow-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-toolbar>
    <v-data-table :headers="headers" :items="dataPorts" class="elevation-1" dark hide-actions>
      <template v-slot:items="props">
        <td>{{ props.item.name }}</td>
        <td class="text-xs">{{ props.item.value }}</td>
        <td class="justify-center layout px-0">
          <v-icon
            small
            class="mr-2"
            @click="editItem(props.item)"
          >
            edit
          </v-icon>
        </td>
      </template>
      <template v-slot:no-data>
      <v-alert :value="true" color="error" icon="warning">
        Server is not Running 😢
      </v-alert>
    </template>
    </v-data-table>
    <v-alert dark :value="updateStatus" transition="scale-transition" type="success">Ports Updated Successfully.</v-alert>
    <br/><br/><br/><br/>
    <processor />
  </div>
</template>

<script>
  import { mapGetters, mapActions } from "vuex";
  import processor from "./processor";
  export default {
    data: () => ({
      dialog: false,
      headers: [
        {
          text: 'Ports',
          align: 'left',
          value: 'name',
          sortable: false
        },
        {
            text: 'Port Name / Path',
            value: 'value',
            sortable: false
        }
      ],
      editedIndex: -1,
      editedItem: {
        value: ''
      },
      defaultItem: {
        name: '',
        value: ''
      }
    }),

    computed:{
      ...mapGetters(['dataPorts', 'availPort', 'updateStatus']),
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Port'
    }},

    watch: {
      dialog (val) {
        val || this.close()
      }
    },

    created () {
      this.getPortdata();
      this.getPortNumbers();
    },

    methods: {
      ...mapActions(["getPortdata", "getPortNumbers", 'updatePortinfo']),

      editItem (item) {
        this.editedIndex = this.dataPorts.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },

      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.dataPorts[this.editedIndex], this.editedItem)
        } else {
          this.dataPorts.push(this.editedItem)
        }
        this.close()
      }
    },

    components: {
      processor
    }
  }
</script>