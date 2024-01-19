<template>
    <Login :login_type="login_type" />
</template>
<script setup>
import Login from '@/components/LoginScreen.vue';
const login_type = "User"
</script>
