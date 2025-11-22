<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <Navbar v-if="authStore.user" />
  <div class="container mt-4">
    <RouterView />
  </div>
</template>

<style>
/* Global styles can go here */
</style>
