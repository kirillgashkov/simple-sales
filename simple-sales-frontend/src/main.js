import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import { useUsersStore } from "./stores/users";

import "./assets/main.scss";

const app = createApp(App);

app.use(createPinia());
app.use(router);

const usersStore = useUsersStore();
await usersStore.loadUser();

app.mount("#app");
