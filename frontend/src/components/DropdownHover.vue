<template>
  <div class="text-center">
    <v-menu open-on-hover>
      <template v-slot:activator="{ props }">
        <v-btn color="#fff" v-bind="props"
          class="title my-2 align-self-center rounded text-center">
          <router-link class="text-decoration-none" v-if="items.length==1" :to="{name:items[0].route}">
            <p>{{ main_title }}</p>
          </router-link>
          <div v-else>
            {{ main_title }}
          </div>
        </v-btn>
      </template>
      <v-list v-if="items.length>1">
        <v-list-item v-for="(item, key) in items" :key="key" :to="{ name : item.route}">
          <v-list-item-title>{{ item.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
export default {
  name: 'DropdownOnHover',
  props: {
    items: Array,
    main_title: String,
  }
}
</script>
<style scoped>
.title:hover {
  color: #ffffff !important;
  background-color: #565656;
}
.v-btn__content {
  font-size: small !important;
}
</style>
