<template>
  <AdminMain :cards="cards" :main="main" />
</template>

<script setup>
import AdminMain from '@/components/AdminMain.vue';
const cards = {
  "SplitMoney": { name: "Split Money" },
  "AllExpenditure": { name: "All Expenditure" },
  "Home": { name: "Logout" },
};
const main = false;
</script>
