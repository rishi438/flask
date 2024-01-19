// Composables
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("@/views/home/Home.vue"),
      },
      {
        path: "user",
        name: "UserLogin",
        component: () => import("@/views/home/UserLogin.vue"),
      },
    ],
  },
  {
    path: "/user",
    components: {
      default: () => import("@/layouts/admin/Default.vue"),
    },
    children: [
      {
        path: "split-money",
        name: "SplitMoney",
        component: () => import("@/views/user/expenses/SplitMoney.vue"),
      },
      {
        path: "all-expenditure",
        name: "AllExpenditure",
        component: () => import("@/views/user/transactions/AllExpenditure.vue"),
      },
    ],
  },
  {
    path: "/user/home",
    components: {
      default: () => import("@/layouts/default/Default.vue"),
    },
    children: [
      {
        path: "",
        name: "UserHome",
        component: () => import("@/views/home/UserHome.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
