<template>
  <v-app id="main_screen">
    <v-spacer></v-spacer>
    <v-main>
      <v-container>
        <v-row>
          <v-col v-for="(card, key) in cards" :key="key" :sm=" main?12:4" cols="12">
            <router-link :to="{ name: key}" class="text-decoration-none">
              <v-sheet :height="50" border rounded class="d-flex justify-center align-center elevation-3" :class="{'py-8': main, 'py-5': !main}">{{card.name}}</v-sheet>
            </router-link>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.v-sheet:hover{
  background-color: #cdcdcd;
}
</style>

<script>
 export default {
    name: 'AdminMain',
    props: {
      cards: Object,
      main: {
        type: Boolean,
        default: false,
    },
 }};
</script>
