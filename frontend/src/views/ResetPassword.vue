<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const password = ref('')
const confirmPassword = ref('')
const message = ref('')
const error = ref('')
const token = route.query.token

const handleReset = async () => {
    if (password.value !== confirmPassword.value) {
        error.value = "Passwords do not match"
        return
    }
    
    try {
        // We need to pass the token in the Authorization header as a Bearer token
        // The backend expects jwt_required() which looks for this header
        const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/reset-password`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ password: password.value })
        })
        
        const data = await res.json()
        if (res.ok) {
            message.value = "Password reset successfully! Redirecting..."
            setTimeout(() => router.push('/login'), 2000)
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
                <h3 class="mb-3">Reset Password</h3>
                <p class="text-muted mb-4">Enter your new password.</p>
                
                <form @submit.prevent="handleReset">
                    <div class="mb-3">
                        <input v-model="password" type="password" class="form-control" placeholder="New Password" required>
                    </div>
                    <div class="mb-3">
                        <input v-model="confirmPassword" type="password" class="form-control" placeholder="Confirm Password" required>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-100 mb-3">Reset Password</button>
                    
                    <div v-if="message" class="alert alert-success">{{ message }}</div>
                    <div v-if="error" class="alert alert-danger">{{ error }}</div>
                </form>
            </div>
        </div>
    </div>
</template>
