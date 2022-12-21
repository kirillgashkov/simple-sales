<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";

import http from "../http";
import { useUsersStore } from "../stores/users";
import router from "../router";

const usersStore = useUsersStore();

const isSignedIn = computed(() => !!usersStore.user);
const isManager = computed(
  () => usersStore.user.employee.employee_type.name === "manager"
);
const user_display_name = computed(
  () => usersStore.user.employee.first_name + " " + usersStore.user.employee.last_name
);

async function signOut() {
  await http.delete("/sessions/current");
  usersStore.removeUser(null);
  router.push({ name: "home" });
}
</script>

<template>
  <nav class="navbar is-light" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <RouterLink class="navbar-item" to="/">
        <img src="@/assets/logo.svg" width="84" height="28">
      </RouterLink>

      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu">
      <template v-if="isSignedIn">
        <div class="navbar-start">
          <template v-if="isManager">
            <div class="navbar-item has-dropdown is-hoverable">
              <RouterLink class="navbar-link is-arrowless" :to="{ name: 'tasks' }">
                Задания
              </RouterLink>

              <div class="navbar-dropdown">
                <RouterLink class="navbar-item" :to="{ name: 'tasks', query: { tab: 'assigned' } }">
                  Назначенные
                </RouterLink>
                <RouterLink class="navbar-item" :to="{ name: 'tasks', query: { tab: 'created' } }">
                  Созданные
                </RouterLink>
                <RouterLink class="navbar-item" :to="{ name: 'tasks', query: { tab: 'all' } }">
                  Все
                </RouterLink>
              </div>
            </div>
          </template>

          <template v-else>
            <RouterLink class="navbar-item" :to="{ name: 'tasks' }">
              Задания
            </RouterLink>
          </template>

          <RouterLink class="navbar-item" :to="{ name: 'clients' }">
            Клиенты
          </RouterLink>

          <RouterLink class="navbar-item" :to="{ name: 'employees' }">
            Сотрудники
          </RouterLink>

          <template v-if="isManager">
            <RouterLink class="navbar-item" :to="{ name: 'reports' }">
              Отчеты
            </RouterLink>
          </template>
        </div>
      </template>

      <div class="navbar-end">
        <div class="navbar-item">
          <template v-if="isSignedIn">
            <div class="navbar-item has-dropdown is-hoverable">
              <RouterLink class="navbar-link" :to="{ name: 'account' }">
                <strong>{{ user_display_name }}</strong>
              </RouterLink>

              <div class="navbar-dropdown">
                <RouterLink class="navbar-item" :to="{ name: 'account' }">
                  Аккаунт
                </RouterLink>
                <hr class="navbar-divider">
                <a class="navbar-item" @click="signOut">
                  Выйти
                </a>
              </div>
            </div>
          </template>

          <template v-else>
            <div class="buttons">
              <RouterLink class="button is-primary" :to="{ name: 'sign-up' }">
                <strong>Зарегистрироваться</strong>
              </RouterLink>
              <RouterLink class="button" :to="{ name: 'sign-in' }">
                Войти
              </RouterLink>
            </div>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>
