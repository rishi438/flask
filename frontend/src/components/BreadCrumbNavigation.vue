<template>
  <v-breadcrumbs :items="navigate_route">
    <template v-slot:divider>
      <v-icon icon="mdi-chevron-right"></v-icon>
    </template>
  </v-breadcrumbs>
</template>
<script >
export default {
  name:"BreadCrumb",
  props:{
    navigate_route:Array
  },
}
</script>
