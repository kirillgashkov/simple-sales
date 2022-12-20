<script setup>
import { RouterLink, RouterView } from "vue-router";
import TheNavbar from "./components/TheNavbar.vue";
</script>

<template>
  <header>
    <TheNavbar />
  </header>

  <RouterView />
</template>
