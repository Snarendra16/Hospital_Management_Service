<script setup>
import { ref } from 'vue'

const email = ref('')
const message = ref('')
const error = ref('')

const handleReset = async () => {
    message.value = ''
    error.value = ''
    
    try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/forgot-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.value })
        })
        
        const data = await res.json()
        if (res.ok) {
            message.value = data.msg
        } else {
            error.value = data.msg
        }
    } catch (e) {
        error.value = 'An error occurred'
    }
}
</script>

<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card shadow-lg p-4" style="max-width: 400px; width: 100%;">
            <div class="card-body text-center">
                <h3 class="mb-3">Forgot Password</h3>
                <p class="text-muted mb-4">Enter your email to receive a reset link.</p>
                
                <form @submit.prevent="handleReset">
                    <div class="mb-3">
                        <input v-model="email" type="email" class="form-control" placeholder="Enter your email" required>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-100 mb-3">Send Reset Link</button>
                    
                    <div v-if="message" class="alert alert-success">{{ message }}</div>
                    <div v-if="error" class="alert alert-danger">{{ error }}</div>
                </form>
                
                <router-link to="/login" class="text-decoration-none">Back to Login</router-link>
            </div>
        </div>
    </div>
</template>
