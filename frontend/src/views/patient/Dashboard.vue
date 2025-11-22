<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const doctors = ref([])
const appointments = ref([])
const searchQuery = ref('')
const selectedDoctor = ref(null)
const booking = ref({ date: '', time: '' })
const profile = ref({ contact_number: '', address: '', date_of_birth: '' })
const showProfile = ref(false)

const fetchProfile = async () => {
    const res = await fetch('http://localhost:5000/patient/profile', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
        const data = await res.json()
        profile.value = {
            contact_number: data.contact_number || '',
            address: data.address || '',
            date_of_birth: data.date_of_birth || ''
        }
    }
}

const updateProfile = async () => {
    const res = await fetch('http://localhost:5000/patient/profile', {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}` 
        },
        body: JSON.stringify(profile.value)
    })
    if (res.ok) {
        alert('Profile updated')
        showProfile.value = false
    }
}

const searchDoctors = async () => {
  let url = 'http://localhost:5000/patient/doctors'
  if (searchQuery.value) {
      url += `?specialization=${searchQuery.value}`
  }
  
  const res = await fetch(url, {
    headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (res.ok) doctors.value = await res.json()
}

const fetchAppointments = async () => {
  const res = await fetch('http://localhost:5000/patient/appointments', {
    headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (res.ok) appointments.value = await res.json()
}

const openBookModal = (doc) => {
    selectedDoctor.value = doc
    booking.value = { date: '', time: '' }
}

const bookAppointment = async () => {
    if (!selectedDoctor.value) return

    const res = await fetch('http://localhost:5000/patient/appointments', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}` 
        },
        body: JSON.stringify({
            doctor_id: selectedDoctor.value.id,
            date: booking.value.date,
            time: booking.value.time
        })
    })

    if (res.ok) {
        alert('Appointment booked successfully')
        selectedDoctor.value = null
        fetchAppointments()
    } else {
        const data = await res.json()
        alert(data.msg || 'Error booking appointment')
    }
}

onMounted(() => {
  searchDoctors()
  fetchAppointments()
  fetchProfile()
})
</script>

<template>
  <div class="fade-in">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Patient Dashboard</h2>
        <div>
            <button class="btn btn-outline-primary me-2" @click="showProfile = true">My Profile</button>
            <span class="badge bg-success rounded-pill px-3 py-2">Welcome, {{ authStore.user.username }}</span>
        </div>
    </div>
    
    <div class="row">
        <!-- Search & Book -->
        <div class="col-md-7">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-white d-flex justify-content-between align-items-center">
                    <h5 class="mb-0 text-primary">Find a Doctor</h5>
                </div>
                <div class="card-body">
                    <div class="input-group mb-4">
                        <span class="input-group-text bg-light border-end-0"><i class="bi bi-search"></i></span>
                        <input v-model="searchQuery" type="text" class="form-control border-start-0 bg-light" placeholder="Search by specialization (e.g. Cardiology)">
                        <button class="btn btn-primary px-4" @click="searchDoctors">Search</button>
                    </div>
                    
                    <div class="row g-3">
                        <div v-for="doc in doctors" :key="doc.id" class="col-12">
                            <div class="card border h-100 hover-card">
                                <div class="card-body d-flex justify-content-between align-items-center">
                                    <div>
                                        <h5 class="card-title mb-1 text-dark">Dr. {{ doc.username }}</h5>
                                        <span class="badge bg-light text-dark border mb-2">{{ doc.specialization }}</span>
                                        <p class="card-text small text-muted mb-0">{{ doc.description || 'No description available.' }}</p>
                                    </div>
                                    <button class="btn btn-outline-primary" @click="openBookModal(doc)">Book Now</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- My Appointments -->
        <div class="col-md-5">
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <h5 class="mb-0 text-primary">My Appointments</h5>
                </div>
                <div class="card-body p-0">
                    <div v-if="appointments.length === 0" class="p-4 text-center text-muted">
                        No appointments found.
                    </div>
                    <div v-else class="list-group list-group-flush">
                        <div v-for="appt in appointments" :key="appt.id" class="list-group-item p-3">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <h6 class="mb-0">Dr. {{ appt.doctor_name }}</h6>
                                    <small class="text-muted">{{ appt.date }} at {{ appt.time }}</small>
                                </div>
                                <span :class="{
                                    'badge bg-warning text-dark': appt.status === 'Booked',
                                    'badge bg-success': appt.status === 'Completed',
                                    'badge bg-danger': appt.status === 'Cancelled'
                                }">{{ appt.status }}</span>
                            </div>
                            <div v-if="appt.treatment" class="mt-2 p-2 bg-light rounded border small">
                                <strong>Diagnosis:</strong> {{ appt.treatment.diagnosis }} <br>
                                <strong>Prescription:</strong> {{ appt.treatment.prescription }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="selectedDoctor" class="modal d-block" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(2px);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border-0 shadow-lg">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">Book Appointment</h5>
                    <button type="button" class="btn-close btn-close-white" @click="selectedDoctor = null"></button>
                </div>
                <div class="modal-body p-4">
                    <p class="mb-3">Booking with <strong>Dr. {{ selectedDoctor.username }}</strong></p>
                    <form @submit.prevent="bookAppointment">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Date</label>
                            <input v-model="booking.date" type="date" class="form-control" required>
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-bold">Time</label>
                            <input v-model="booking.time" type="time" class="form-control" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Confirm Booking</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Profile Modal -->
    <div v-if="showProfile" class="modal d-block" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(2px);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border-0 shadow-lg">
                <div class="modal-header bg-info text-white">
                    <h5 class="modal-title">My Profile</h5>
                    <button type="button" class="btn-close btn-close-white" @click="showProfile = false"></button>
                </div>
                <div class="modal-body p-4">
                    <form @submit.prevent="updateProfile">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Contact Number</label>
                            <input v-model="profile.contact_number" type="text" class="form-control">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Address</label>
                            <textarea v-model="profile.address" class="form-control" rows="2"></textarea>
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-bold">Date of Birth</label>
                            <input v-model="profile.date_of_birth" type="date" class="form-control">
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-info text-white btn-lg">Update Profile</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
.hover-card:hover {
    background-color: #f8f9fa;
    border-color: #4e73df !important;
    cursor: pointer;
}
</style>
