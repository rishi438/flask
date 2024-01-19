<template>
    <BreadCrumbNavigation :navigate_route="navigate_route" class="my-3"/>
    <div class="my-3">
        <data-table ref="data_table" :status="status" :data="table_data" :headers="table_header" :items_in_page="items_per_page"/>
    </div>
</template>

<script>
import BreadCrumbNavigation from '@/components/BreadCrumbNavigation.vue';
import DataTable from './DataTable.vue';
export default {
  name: 'AllExpenditure',
  components: {
    DataTable,
  },
  props: {
    page_title: String,
    table_headers: Array,
  },
  computed: {
    table_header() {
      return this.table_headers;
    },
  },
  data() {
    return {
      table_data: this.table_data,
      items_per_page: 5,
      selected_file: null,
      status:false,
    };
  },
};
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
</script>
