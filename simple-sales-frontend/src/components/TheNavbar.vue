<script setup>
import { RouterLink } from "vue-router";
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
      <div class="navbar-start">
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

        <RouterLink class="navbar-item" :to="{ name: 'clients' }">
          Клиенты
        </RouterLink>

        <RouterLink class="navbar-item" :to="{ name: 'employees' }">
          Сотрудники
        </RouterLink>

        <RouterLink class="navbar-item" :to="{ name: 'reports' }">
          Отчеты
        </RouterLink>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-primary">
              <strong>Зарегистрироваться</strong>
            </a>
            <a class="button">
              Войти
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
