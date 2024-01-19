<template>
    <BreadCrumbNavigation :navigate_route="navigate_route" class="my-3"/>
    <div class="my-3">
        <data-table ref="data_table" :status="status" :data="table_data" :headers="table_headers" :items_in_page="items_per_page"/>
    </div>
</template>

<script>
import BreadCrumbNavigation from '@/components/BreadCrumbNavigation.vue';
import DataTable from '@/components/DataTable.vue';
export default {
  name: 'AllExpenditure',
  components: {
    DataTable,
  },
  props: {
    page_title: String,
  },
  data() {
    return {
      table_headers: [
        { title: 'Balance ID', align: 'start', key: 'balance_id' },
        { title: 'Creditor ID', align: 'end', key: 'creditor_id' },
        { title: 'Debitor ID', align: 'end', key: 'debitor_id' },
        { title: 'Amount', align: 'end', key: 'amount' },
      ],
      table_data: [{ balance_id: "fcf5f4de-e7ad-493d-924e-6813c3f20e7c", creditor_id: "b095f9f4-8208-4f75-92d3-10043d0d12ff", debitor_id: "2c91b44f-a3c7-4fa5-b005-5f52842b9f4b", amount: 1000 }],
      items_per_page: 10,
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
