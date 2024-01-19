<template>
  <v-card>
    <v-card-title search_status="search_status">
      <v-spacer></v-spacer>
      <v-row class="py-3">
        <v-col sm="6" cols="12" class="align-self-center">
          <v-select class="px-0" label="Select Field" :items="headers" :item-value="headers" v-model.lazy="search_param"
            ></v-select>
        </v-col>
        <v-col sm="6" cols="12" class="align-self-center mt-2 pb-5">
          <v-row>
            <v-text-field :label="`${search_param ? 'Enter ' + search_param : 'Disabled'}`" class="mx-5" v-model="search_value" clearable
            :rules="[(value) => {
              if (value) {
                return true;
              } else {
                return 'This field is required';
              }
            }]"
              single-line :disabled="!search_param || !status" :lazy="true" ref="second_field" >
            </v-text-field>
            <v-btn :disabled="!search_param || !status?!btn_state:btn_state" class="mr-5" icon="mdi-magnify" @click="search_btn">
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-card-title>
    <v-data-table :search="search" :custom-filter="filter_data" v-bind:items-per-page="items_in_page ? items_in_page : 0" :headers="headers" :items="data" class="elevation-1"  hide-header></v-data-table>
  </v-card>
</template>

<script>
import { VDataTable } from 'vuetify/labs/VDataTable'
export default {
  components: {
    VDataTable,
  },
  props: {
    headers: Array,
    data: Array,
    items_in_page: Number,
    status: {
      type: Boolean,
      default: true,
    },
    page_title: String,
    search_status: String,
  },
  data() {
    return {
      search_param: null,
    btn_state: false,
    search_value:'',
    search:'',
    }
  },
  methods: {
    clear_fields(){
      if(this.status){
        this.reset_validation();
        this.btn_state=false
      }
    },
    search_btn(){
      this.search=this.search_value;
      console.log(this.search_param,this.search)
    },
    reset_validation(flag=false){
      this.search_param=flag?'':this.search_param;
      this.$refs.second_field.reset();
      this.$refs.second_field.resetValidation();
    },
    filter_data(value, query,items) {
        return items[this.search_param.toLowerCase().replaceAll(" ","_")].toLowerCase().toString().includes(query);
    }
  },
};
</script>
