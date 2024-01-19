<template>
  <AdminMain :cards="cards" :main="main" />
</template>

<script setup>
import AdminMain from '@/components/AdminMain.vue';
const cards = {
  "UserLogin": { name: "User Login" },
};
const main = true
</script>
