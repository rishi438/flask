<template>
    <BreadCrumbNavigation :navigate_route="navigate_route" class="my-3"/>
    <v-container class="my-5">
        <div class="title text-center">
            Search Information
          </div>
        <card class="my-5" :users="users_list" :bill_types="bill_types" @formSubmit="handleFormSubmit"/>
    </v-container>
</template>

<style scoped>
.title{
    font-size: xx-large;
}
</style>

<script setup>
import Card from '@/components/CardConf.vue';
import BreadCrumbNavigation from '@/components/BreadCrumbNavigation.vue';
const name = "SplitMoney";
const navigate_route=[
    {
        title: "home",
        disabled: false,
        href: "home",
    },
    {
        title: name,
        disabled: true,
        href: name,
    },
]
const users_list=["33c24a55-3068-4092-a4e0-3a89a0a7b5c9","2c91b44f-a3c7-4fa5-b005-5f52842b9f4b"]
const bill_types=["EXACT","EQUAL","PERCENTAGE"]
</script>
