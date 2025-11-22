<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    const role = await authStore.login(username.value, password.value)
    router.push('/' + role)
  } catch (err) {
    error.value = 'Invalid username or password'
  }
}
</script>

<template>
  <div class="container fade-in">
    <div class="row justify-content-center align-items-center min-vh-80">
      <div class="col-md-5">
        <div class="text-center mb-5">
          <h1 class="display-4 fw-bold text-primary">Welcome Back</h1>
          <p class="lead text-muted">Hospital Registry</p>
        </div>
        <div class="card shadow-lg border-0">
          <div class="card-body p-5">
            <h3 class="text-center mb-4">Login</h3>
            <div v-if="error" class="alert alert-danger rounded-pill text-center">{{ error }}</div>
            <form @submit.prevent="handleLogin">
              <div class="mb-4">
                <label class="form-label text-uppercase small fw-bold text-muted">Username</label>
                <input v-model="username" type="text" class="form-control form-control-lg" placeholder="Enter your username" required>
              </div>
              <div class="mb-4">
                <label class="form-label text-uppercase small fw-bold text-muted">Password</label>
                <input v-model="password" type="password" class="form-control form-control-lg" placeholder="Enter your password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100 btn-lg mb-3">Sign In</button>
            </form>
            <div class="text-center mt-4">
              <p class="small text-muted mb-2">Don't have an account?</p>
              <div class="d-flex justify-content-center gap-3">
                <router-link to="/register" class="text-decoration-none fw-bold">Patient Register</router-link>
                <span class="text-muted">|</span>
                <router-link to="/register-doctor" class="text-decoration-none fw-bold">Doctor Register</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.min-vh-80 {
  min-height: 80vh;
}
</style>
