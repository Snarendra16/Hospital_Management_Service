<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const stats = ref({ doctors: 0, patients: 0, appointments: 0 })
const doctors = ref([])
const showAddDoctor = ref(false)
const newDoctor = ref({ username: '', email: '', password: '', specialization: '', description: '' })

const fetchStats = async () => {
  const res = await fetch('http://localhost:5000/admin/stats', {
    headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (res.ok) stats.value = await res.json()
}

const fetchDoctors = async () => {
  const res = await fetch('http://localhost:5000/admin/doctors', {
    headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (res.ok) doctors.value = await res.json()
}

const addDoctor = async () => {
  const res = await fetch('http://localhost:5000/admin/doctors', {
    method: 'POST',
    headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}` 
    },
    body: JSON.stringify(newDoctor.value)
  })
  
  if (res.ok) {
      alert('Doctor added successfully')
      showAddDoctor.value = false
      fetchDoctors()
      fetchStats()
      newDoctor.value = { username: '', email: '', password: '', specialization: '', description: '' }
  } else {
      const data = await res.json()
      alert(data.msg || 'Error adding doctor')
  }
}

const blockUser = async (doctor) => {
    if (!confirm(`Are you sure you want to ${doctor.is_active ? 'block' : 'unblock'} this doctor?`)) return

    const res = await fetch(`http://localhost:5000/admin/users/${doctor.user_id}/block`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    
    if (res.ok) {
        fetchDoctors()
    } else {
        alert('Error updating status')
    }
}

const triggerTask = async (taskName) => {
    const res = await fetch(`http://localhost:5000/admin/tasks/${taskName}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const data = await res.json()
    alert(data.msg)
}

onMounted(() => {
  fetchStats()
  fetchDoctors()
})
</script>

<template>
  <div class="fade-in">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Admin Dashboard</h2>
        <span class="badge bg-primary rounded-pill px-3 py-2">Welcome, Admin</span>
    </div>
    
    <!-- Stats -->
    <div class="row mb-5">
      <div class="col-md-4">
        <div class="card text-white bg-gradient-primary mb-3 h-100">
          <div class="card-body d-flex flex-column justify-content-between">
            <h5 class="card-title text-uppercase small opacity-75">Total Doctors</h5>
            <p class="card-text display-4 fw-bold">{{ stats.doctors }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-gradient-success mb-3 h-100">
          <div class="card-body d-flex flex-column justify-content-between">
            <h5 class="card-title text-uppercase small opacity-75">Total Patients</h5>
            <p class="card-text display-4 fw-bold">{{ stats.patients }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-gradient-info mb-3 h-100">
          <div class="card-body d-flex flex-column justify-content-between">
            <h5 class="card-title text-uppercase small opacity-75">Total Appointments</h5>
            <p class="card-text display-4 fw-bold">{{ stats.appointments }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- System Tasks -->
    <div class="row mb-5">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <h5 class="mb-0 text-dark">System Tasks</h5>
                </div>
                <div class="card-body d-flex gap-3">
                    <button class="btn btn-outline-primary" @click="triggerTask('reminders')">
                        <i class="bi bi-bell"></i> Send Daily Reminders
                    </button>
                    <button class="btn btn-outline-success" @click="triggerTask('report')">
                        <i class="bi bi-file-earmark-text"></i> Generate Monthly Report
                    </button>
                    <button class="btn btn-outline-info" @click="triggerTask('export')">
                        <i class="bi bi-download"></i> Export Treatments CSV
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Manage Doctors -->
    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center bg-white">
        <h5 class="mb-0 text-primary">Manage Doctors</h5>
        <button class="btn btn-primary btn-sm" @click="showAddDoctor = !showAddDoctor">
            <i class="bi bi-plus-lg"></i> {{ showAddDoctor ? 'Cancel' : 'Add New Doctor' }}
        </button>
      </div>
      <div class="card-body">
        
        <!-- Add Doctor Form -->
        <div v-if="showAddDoctor" class="mb-4 p-4 bg-light rounded shadow-sm">
            <h6 class="mb-3">New Doctor Details</h6>
            <form @submit.prevent="addDoctor">
                <div class="row g-3">
                    <div class="col-md-6">
                        <input v-model="newDoctor.username" placeholder="Username" class="form-control" required>
                    </div>
                    <div class="col-md-6">
                        <input v-model="newDoctor.email" type="email" placeholder="Email" class="form-control" required>
                    </div>
                    <div class="col-md-6">
                        <input v-model="newDoctor.password" type="password" placeholder="Password" class="form-control" required>
                    </div>
                    <div class="col-md-6">
                        <input v-model="newDoctor.specialization" placeholder="Specialization" class="form-control" required>
                    </div>
                    <div class="col-12">
                        <textarea v-model="newDoctor.description" placeholder="Description (Optional)" class="form-control" rows="2"></textarea>
                    </div>
                    <div class="col-12 text-end">
                        <button type="submit" class="btn btn-success px-4">Save Doctor</button>
                    </div>
                </div>
            </form>
        </div>

        <!-- Doctors List -->
        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Specialization</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="doc in doctors" :key="doc.id">
                        <td>#{{ doc.id }}</td>
                        <td class="fw-bold">{{ doc.username }}</td>
                        <td><span class="badge bg-light text-dark border">{{ doc.specialization }}</span></td>
                        <td>
                            <span :class="doc.is_active ? 'badge bg-success' : 'badge bg-danger'">
                                {{ doc.is_active ? 'Active' : 'Blocked' }}
                            </span>
                        </td>
                        <td>
                            <button class="btn btn-sm" 
                                :class="doc.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                                @click="blockUser(doc)">
                                {{ doc.is_active ? 'Block' : 'Unblock' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-gradient-primary {
    background: linear-gradient(45deg, #4e73df, #224abe);
}
.bg-gradient-success {
    background: linear-gradient(45deg, #1cc88a, #13855c);
}
.bg-gradient-info {
    background: linear-gradient(45deg, #36b9cc, #258391);
}
</style>
