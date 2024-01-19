<template>
  <v-card class="mx-auto py-3 elevation-5" max-width="500" variant="outlined">
    <v-card-item>
      <v-form @submit.prevent="handle_form">
        <v-autocomplete
        class="px-0"
        clearable
        label="Type of Bill Sharing"
        :items="bill_types"
        v-model="selected_bill_type"
        @click:clear="clear_text"
        @input="clear_text"
        ></v-autocomplete>
        <v-autocomplete
        class="px-0"
        clearable
        :multiple="!(selected_bill_type !== 'EQUAL')"
        label="Choose bill-sharing recipients:"
        :items="users"
        v-model="selected_user"
        @click:clear="clear_text"
        @update:change="clear_text"
      >
      </v-autocomplete>
        <div>
          <div class="d-flex justify-even">
            <v-text-field
            clearable
            v-show="selected_bill_type == 'PERCENTAGE' || selected_bill_type=='EXACT' "
            :label="`${selected_bill_type=='EXACT'?'Enter bill amount ':selected_bill_type=='PERCENTAGE'?'Enter bill percentage':'Disabled'}`"
            :rules="[(value)=>{
              if (!value) return 'This field is required';
              const regex = /^\d+(\.\d+)?$/;
              if (!regex.test(value)) return 'Please enter a valid number';add_btn=false;
              let=amount = parseFloat(value);
              if (!Number.isFinite(amount)) return 'Please enter a finite number';add_btn=false;
              if (amount > 100) return 'Maximum allowed value is 100';add_btn=false;
              add_btn=true;
              return true;
          }]"
            :lazy="true"
            @click:clear="btn_state=false"
            v-model="share_amount_perc"
            ref="first_field"
          ></v-text-field>
            <v-btn class="bg-blue justify-end ml-2" variant="outlined" :disabled="!(selected_bill_type!='EQUAL' && share_amount_perc && add_btn)" v-if="selected_bill_type=='PERCENTAGE'|| selected_bill_type=='EXACT'"  @click="add_shares"> ADD </v-btn>
          </div>
          <div class="py-2 my-3 d-flex justify-center bg-red-accent-1 text-white" v-if="selected_bill_type!='EQUAL'" v-for="(value,index) in shares" :key="index"> {{ Object.keys(value)[0] }} - {{Object.values(value)[0] }}</div>
        </div>
        <v-text-field
          clearable
          v-show="selected_bill_type === 'PERCENTAGE' || selected_bill_type=='EQUAL'"
          :label="'Enter bill amount'"
          :rules="[(value)=>{
            if (!value) return 'This field is required';
            const regex = /^\d+(\.\d+)?$/;
            if (!regex.test(value)) return 'Please enter a valid number';
            let=amount = parseFloat(value);
            if (!Number.isFinite(amount)) return 'Please enter a finite number';
            if (amount > 10000000) return 'Maximum allowed value is 1,00,00,000';
            return true;
        }]"
          v-model="total_amount"
          :lazy="true"
          @click:clear="btn_state=false"
          ref="second_field"
      ></v-text-field>
        <v-btn class="ml-3" variant="outlined" type="submit" > PAY </v-btn>
      </v-form>
    </v-card-item>
  </v-card>
</template>

<script>
export default {
  props: {
    users: Array,
    bill_types: Array
  },
  data: () => ({
    selected_user: null,
    add_btn:false,
    total_amount:null,
    selected_bill_type:null,
    share_amount_perc:null,
    shares: [],
  }),
  methods: {
    add_shares() {
      if (this.selected_user && this.share_amount_perc) {
        let share_object={}
        share_object[this.selected_user] = this.share_amount_perc
        this.shares.push(share_object)
        this.selected_user = null;
        this.share_amount_perc = null;
        this.$refs.first_field.reset();
        this.$refs.second_field.reset();
      }
    },
    clear_text(){
      this.$refs.first_field.reset()
      this.$refs.second_field.reset()
      this.$refs.first_field.resetValidation()
      this.$refs.second_field.resetValidation()
      this.shares=[]
    },
    handle_form(){
      console.log("Selected User:", this.selected_user);
      console.log("Share Amount Percentage:", this.share_amount_perc);
      console.log("Total Amount:", this.total_amount);
      console.log("Shares:", this.shares);
    }
  },
}
</script>
