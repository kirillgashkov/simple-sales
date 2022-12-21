import { createRouter, createWebHistory } from "vue-router";
import { useUsersStore } from "../stores/users";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/sign-in",
      name: "sign-in",
      component: () => import("../views/SignInView.vue"),
    },
    {
      path: "/sign-up",
      name: "sign-up",
      component: () => import("../views/SignUpView.vue"),
    },
    {
      path: "/account",
      name: "account",
      component: () => import("../views/AccountView.vue"),
    },
    {
      path: "/tasks",
      name: "tasks",
      component: () => import("../views/TasksView.vue"),
    },
    {
      path: "/tasks/:id",
      name: "task",
      component: () => import("../views/TaskView.vue"),
      props: true,
    },
    {
      path: "/clients",
      name: "clients",
      component: () => import("../views/ClientsView.vue"),
    },
    {
      path: "/clients/:id",
      name: "client",
      component: () => import("../views/ClientView.vue"),
      props: true,
    },
    {
      path: "/clients/:clientId/contacts/:contactId",
      name: "contact",
      component: () => import("../views/ContactView.vue"),
      props: true,
    },
    {
      path: "/clients/:clientId/contracts/:contractId",
      name: "contract",
      component: () => import("../views/ContractView.vue"),
      props: true,
    },
    {
      path: "/employees",
      name: "employees",
      component: () => import("../views/EmployeesView.vue"),
    },
    {
      path: "/employees/:id",
      name: "employee",
      component: () => import("../views/EmployeeView.vue"),
      props: true,
    },
    {
      path: "/reports",
      name: "reports",
      component: () => import("../views/ReportsView.vue"),
    },
  ],
});

router.beforeEach((to, from) => {
  const usersStore = useUsersStore();

  if (!usersStore.isUserLoaded) {
    usersStore.loadUser();
  }

  if (!usersStore.user && to.name !== "sign-in") {
    return { name: "sign-in" };
  }
});

export default router;
