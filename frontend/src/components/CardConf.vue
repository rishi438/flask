<template>
  <v-card class="mx-auto py-3 elevation-5" max-width="500" variant="outlined">
    <v-card-item>
      <v-form @submit.prevent="handle_form">
        <v-autocomplete class="px-0" clearable label="Type of Bill Sharing" :items="bill_types"
          v-model="selected_bill_type" @click:clear="clear_text" @input="clear_text"></v-autocomplete>
        <v-autocomplete class="px-0" clearable :multiple="!(selected_bill_type !== 'EQUAL')"
          label="Choose bill-sharing recipients:" :items="users" v-model="selected_user" @click:clear="clear_text"
          @update:change="clear_text" ref="first_field">
        </v-autocomplete>
        <div>
          <div class="d-flex justify-even">
            <v-text-field clearable v-show="selected_bill_type == 'PERCENTAGE' || selected_bill_type == 'EXACT'"
              :label="`${selected_bill_type == 'EXACT' ? 'Enter bill amount ' : selected_bill_type == 'PERCENTAGE' ? 'Enter bill percentage' : 'Disabled'}`"
              :rules="[(value) => {
                if (shares.length === 0) {
                  if (!value) return 'This field is required';
                  const regex = /^\d+(\.\d+)?$/;
                  if (!regex.test(value)) return 'Please enter a valid number'; add_btn = false;
                  let amount = parseFloat(value);
                  if (!Number.isFinite(amount)) return 'Please enter a finite number'; add_btn = false;
                  if (selected_bill_type == 'EXACT' && amount > 10000000) return 'Maximum allowed value is 1,00,00,000'; add_btn = false;
                  if (selected_bill_type == 'PERCENTAGE' && amount > 100) return 'Maximum allowed value is 100'; add_btn = false;
                  add_btn = true;
                  return true;
                }
              }]" :lazy="true" @click:clear="btn_state = false" v-model="share_amount_perc"
              ref="second_field"></v-text-field>
            <v-btn class="bg-blue justify-end ml-2" variant="outlined"
              :disabled="!(selected_bill_type != 'EQUAL' && share_amount_perc && add_btn)"
              v-if="selected_bill_type == 'PERCENTAGE' || selected_bill_type == 'EXACT'" @click="add_shares"> ADD </v-btn>
          </div>
          <div class="py-2 my-3 d-flex justify-center bg-red-accent-1 text-white" v-if="selected_bill_type != 'EQUAL'">
             <div v-for="(value, index) in shares" :key="index">{{ value["user_id"] }} - {{ value["amount"] }}</div></div>
        </div>
        <v-text-field clearable v-show="selected_bill_type === 'PERCENTAGE' || selected_bill_type == 'EQUAL'"
          :label="'Enter bill amount'" :rules="[(value) => {
            if (!value) return 'This field is required';
            const regex = /^\d+(\.\d+)?$/;
            if (!regex.test(value)) return 'Please enter a valid number';
            let amount = parseFloat(value);
            if (!Number.isFinite(amount)) return 'Please enter a finite number';
            if (amount > 10000000) return 'Maximum allowed value is 1,00,00,000';
            return true;
          }]" v-model="total_amount" :lazy="true" @click:clear="btn_state = false" ref="third_field"></v-text-field>
        <v-btn class="ml-3" variant="outlined" type="submit"> PAY </v-btn>
      </v-form>
    </v-card-item>
  </v-card>
</template>

<script>
import axios from 'axios';
import { isProxy, toRaw } from 'vue';
export default {
  props: {
    users: Array,
    bill_types: Array,
    formSubmitCallback: Function
  },
  data: () => ({
    selected_user: [],
    add_btn: false,
    total_amount: 0,
    selected_bill_type: null,
    share_amount_perc: 0,
    participants:[],
    shares: [],
  }),
  methods: {
    add_shares() {
      if (this.selected_user && this.share_amount_perc) {
        const share_object = {};
        share_object["amount"] = parseInt(this.share_amount_perc, 10);
        share_object["user_id"] = this.selected_user;
        this.participants.push(this.selected_user);
        let plainObject = { ...share_object };
        this.shares.push(plainObject);
        this.share_amount_perc = 0;
        this.$refs.first_field.reset();
      }
    },
    clear_text() {
      this.$refs.first_field.reset()
      this.$refs.second_field.reset()
      this.$refs.third_field.reset()
      this.$refs.first_field.resetValidation()
      this.$refs.third_field.resetValidation()
      this.shares = []
    },
    handle_form() {
      this.current_user = "89cbef9f-ccc3-43fd-afd7-8da78d57c783";
      // console.log(          {
      //       amount:parseInt(this.total_amount, 10),
      //       payer:this.current_user,
      //       type:this.selected_bill_type,
      //       participants:[...this.participants],
      //       shares:isProxy(this.shares)?toRaw(this.shares):''
      //     })
      axios
          .post("http://127.0.0.1:5000/api/add-expense/",
          {
            amount:parseInt(this.total_amount, 10),
            payer:this.current_user,
            type:this.selected_bill_type,
            participants:[...this.participants],
            shares:isProxy(this.shares)?toRaw(this.shares):''
          })
          .then(res=>{
            console.log(res.data)
          })
          .catch(err=>{
            console.error(err)
          });
    },
  },
}
</script>
