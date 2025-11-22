<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const appointments = ref([])
const selectedAppointment = ref(null)
const treatment = ref({ diagnosis: '', prescription: '', notes: '' })

const fetchAppointments = async () => {
  const res = await fetch('http://localhost:5000/doctor/appointments', {
    headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (res.ok) appointments.value = await res.json()
}

const openCompleteModal = (appt) => {
    selectedAppointment.value = appt
    treatment.value = { diagnosis: '', prescription: '', notes: '' }
}

const completeAppointment = async () => {
    if (!selectedAppointment.value) return

    const res = await fetch(`http://localhost:5000/doctor/appointments/${selectedAppointment.value.id}/complete`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}` 
        },
        body: JSON.stringify(treatment.value)
    })

    if (res.ok) {
        alert('Appointment completed')
        selectedAppointment.value = null
        fetchAppointments()
    } else {
        alert('Error completing appointment')
    }
}

const patients = ref([])
const selectedPatientHistory = ref(null)
const showHistoryModal = ref(false)
const availability = ref({
    Mon: { active: false, start: '09:00', end: '17:00' },
    Tue: { active: false, start: '09:00', end: '17:00' },
    Wed: { active: false, start: '09:00', end: '17:00' },
    Thu: { active: false, start: '09:00', end: '17:00' },
    Fri: { active: false, start: '09:00', end: '17:00' },
    Sat: { active: false, start: '09:00', end: '17:00' },
    Sun: { active: false, start: '09:00', end: '17:00' }
})

const fetchAvailability = async () => {
    const res = await fetch('http://localhost:5000/doctor/availability', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
        const data = await res.json()
        if (Object.keys(data).length > 0) {
            availability.value = { ...availability.value, ...data }
        }
    }
}

const saveAvailability = async () => {
    const res = await fetch('http://localhost:5000/doctor/availability', {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}` 
        },
        body: JSON.stringify(availability.value)
    })
    if (res.ok) alert('Availability saved')
}

const fetchPatients = async () => {
    const res = await fetch('http://localhost:5000/doctor/patients', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) patients.value = await res.json()
}

const viewHistory = async (patientId) => {
    const res = await fetch(`http://localhost:5000/doctor/patients/${patientId}/history`, {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
        selectedPatientHistory.value = await res.json()
        showHistoryModal.value = true
    }
}

onMounted(() => {
  fetchAppointments()
  fetchPatients()
  fetchAvailability()
})
</script>

<template>
  <div class="fade-in">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Doctor Dashboard</h2>
        <span class="badge bg-info text-white rounded-pill px-3 py-2">Dr. {{ authStore.user.username }}</span>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-white">
                    <h5 class="mb-0 text-primary">Upcoming Appointments</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th>Date/Time</th>
                                    <th>Patient</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appt in appointments" :key="appt.id">
                                    <td>
                                        <div class="fw-bold">{{ appt.date }}</div>
                                        <div class="small text-muted">{{ appt.time }}</div>
                                    </td>
                                    <td>{{ appt.patient_name }}</td>
                                    <td>
                                        <span :class="{
                                            'badge bg-warning text-dark': appt.status === 'Booked',
                                            'badge bg-success': appt.status === 'Completed',
                                            'badge bg-danger': appt.status === 'Cancelled'
                                        }">{{ appt.status }}</span>
                                    </td>
                                    <td>
                                        <button v-if="appt.status === 'Booked'" 
                                                class="btn btn-sm btn-primary"
                                                @click="openCompleteModal(appt)">
                                            Consult
                                        </button>
                                    </td>
                                </tr>
                                <tr v-if="appointments.length === 0">
                                    <td colspan="4" class="text-center py-4 text-muted">No appointments found.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

            </div>
        </div>

        <div class="col-lg-4">
            <!-- Availability -->
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-white d-flex justify-content-between align-items-center">
                    <h5 class="mb-0 text-primary">Weekly Availability</h5>
                    <button class="btn btn-sm btn-primary" @click="saveAvailability">Save</button>
                </div>
                <div class="card-body">
                    <div v-for="(val, day) in availability" :key="day" class="mb-2 d-flex align-items-center justify-content-between">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" v-model="val.active">
                            <label class="form-check-label fw-bold">{{ day }}</label>
                        </div>
                        <div v-if="val.active" class="d-flex gap-1">
                            <input type="time" v-model="val.start" class="form-control form-control-sm" style="width: 80px">
                            <span class="align-self-center">-</span>
                            <input type="time" v-model="val.end" class="form-control form-control-sm" style="width: 80px">
                        </div>
                        <div v-else class="text-muted small">Unavailable</div>
                    </div>
                </div>
            </div>

            <!-- My Patients -->
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <h5 class="mb-0 text-primary">My Patients</h5>
                </div>
                <div class="card-body p-0">
                    <div class="list-group list-group-flush">
                        <div v-for="p in patients" :key="p.id" class="list-group-item d-flex justify-content-between align-items-center p-3">
                            <div>
                                <h6 class="mb-0">{{ p.username }}</h6>
                                <small class="text-muted">ID: #{{ p.id }}</small>
                            </div>
                            <button class="btn btn-sm btn-outline-info" @click="viewHistory(p.id)">History</button>
                        </div>
                        <div v-if="patients.length === 0" class="p-3 text-center text-muted">No patients assigned yet.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- History Modal -->
    <div v-if="showHistoryModal" class="modal d-block" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(2px);">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content border-0 shadow-lg">
                <div class="modal-header bg-light">
                    <h5 class="modal-title">Patient History</h5>
                    <button type="button" class="btn-close" @click="showHistoryModal = false"></button>
                </div>
                <div class="modal-body">
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead class="table-light">
                                <tr>
                                    <th>Date</th>
                                    <th>Doctor</th>
                                    <th>Diagnosis</th>
                                    <th>Prescription</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(h, index) in selectedPatientHistory" :key="index">
                                    <td>{{ h.date }}</td>
                                    <td>Dr. {{ h.doctor }}</td>
                                    <td>{{ h.diagnosis }}</td>
                                    <td>{{ h.prescription }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-if="selectedPatientHistory && selectedPatientHistory.length === 0" class="text-center py-3 text-muted">
                        No medical history found.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Complete Appointment Modal -->
    <div v-if="selectedAppointment" class="modal d-block" style="background: rgba(0,0,0,0.5); backdrop-filter: blur(2px);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border-0 shadow-lg">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">Consultation Details</h5>
                    <button type="button" class="btn-close btn-close-white" @click="selectedAppointment = null"></button>
                </div>
                <div class="modal-body p-4">
                    <form @submit.prevent="completeAppointment">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Diagnosis</label>
                            <textarea v-model="treatment.diagnosis" class="form-control" rows="2" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Prescription</label>
                            <textarea v-model="treatment.prescription" class="form-control" rows="3" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Notes</label>
                            <textarea v-model="treatment.notes" class="form-control" rows="2"></textarea>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-success btn-lg">Complete Consultation</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
