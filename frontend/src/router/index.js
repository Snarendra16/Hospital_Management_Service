import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import RegisterDoctor from '../views/RegisterDoctor.vue'
// Lazy load dashboards
const AdminDashboard = () => import('../views/admin/Dashboard.vue')
const DoctorDashboard = () => import('../views/doctor/Dashboard.vue')
const PatientDashboard = () => import('../views/patient/Dashboard.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/register-doctor',
      name: 'register-doctor',
      component: RegisterDoctor
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/doctor',
      name: 'doctor',
      component: DoctorDashboard,
      meta: { requiresAuth: true, role: 'doctor' }
    },
    {
      path: '/patient',
      name: 'patient',
      component: PatientDashboard,
      meta: { requiresAuth: true, role: 'patient' }
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/register-doctor'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  if (loggedIn) {
    const user = JSON.parse(loggedIn);
    if (to.meta.role && to.meta.role !== user.role) {
      // Redirect to correct dashboard if role mismatch
      return next('/' + user.role);
    }
  }

  next();
})

export default router
