import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user  = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  function setAuth(data) {
    token.value = data.access_token
    user.value  = data.user
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function login(email, password) {
    const res = await axios.post(`${BASE_URL}/api/auth/login`, { email, password })
    setAuth(res.data)
    return res.data
  }

  async function register(email, username, password) {
    const res = await axios.post(`${BASE_URL}/api/auth/register`, { email, username, password })
    setAuth(res.data)
    return res.data
  }

  return { token, user, isAuthenticated, login, register, logout }
})