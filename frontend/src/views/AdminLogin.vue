<template>
  <v-container>
    <h2>Admin Login</h2>
    <v-text-field v-model="email" label="Email"></v-text-field>
    <v-text-field v-model="password" label="Password" type="password"></v-text-field>
    <v-btn color="primary" @click="login">Login</v-btn>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  data() {
    return { email: '', password: '' }
  },
  methods: {
    login() {
      api.post('/admin/login', {
        email: this.email,
        password: this.password
      })
      .then(res => {
        localStorage.setItem('admin', JSON.stringify(res.data.admin))
        this.$router.push({ name: 'AdminDashboard' })
      })
      .catch(() => alert('Invalid credentials'))
    }
  }
}
</script>
