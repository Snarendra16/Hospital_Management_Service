<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const handleRegister = async () => {
  try {
    const response = await fetch('http://localhost:5000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            username: username.value, 
            email: email.value, 
            password: password.value 
        })
    });
    
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.msg || 'Registration failed');
    }
    
    router.push('/login');
  } catch (err) {
    error.value = err.message;
  }
}
</script>

<template>
  <div class="container fade-in">
    <div class="row justify-content-center align-items-center min-vh-80">
      <div class="col-md-5">
        <div class="card shadow-lg border-0">
          <div class="card-body p-5">
            <h3 class="text-center mb-4 text-success">Patient Registration</h3>
            <div v-if="error" class="alert alert-danger rounded-pill text-center">{{ error }}</div>
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label class="form-label text-uppercase small fw-bold text-muted">Username</label>
                <input v-model="username" type="text" class="form-control form-control-lg" required>
              </div>
              <div class="mb-3">
                <label class="form-label text-uppercase small fw-bold text-muted">Email</label>
                <input v-model="email" type="email" class="form-control form-control-lg" required>
              </div>
              <div class="mb-4">
                <label class="form-label text-uppercase small fw-bold text-muted">Password</label>
                <input v-model="password" type="password" class="form-control form-control-lg" required>
              </div>
              <button type="submit" class="btn btn-success w-100 btn-lg mb-3">Create Account</button>
            </form>
            <div class="text-center mt-3">
              <router-link to="/login" class="text-decoration-none">Already have an account? <span class="fw-bold">Login</span></router-link>
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
