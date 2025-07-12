<template>
  <v-container>
    <h2 class="mb-4">Create an Account</h2>

    <v-text-field v-model="name" label="Full Name" outlined></v-text-field>
    <v-text-field v-model="email" label="Email" outlined></v-text-field>
    <v-text-field v-model="phone" label="Phone Number" outlined></v-text-field>
    <v-text-field v-model="address" label="Address" outlined></v-text-field>
    <v-text-field v-model="password" label="Password" type="password" outlined></v-text-field>
    <v-text-field v-model="confirmPassword" label="Confirm Password" type="password" outlined></v-text-field>

    <v-btn color="primary" block class="mt-4" @click="register">Register</v-btn>
  </v-container>
</template>

<script>
import axios from 'axios'
import api from '@/utils/api'

export default {
  name: 'Register',
  data() {
    return {
      name: '',
      email: '',
      phone: '',
      address: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    register() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match.")
        return
      }

      api.post("/register", {
      // axios.post("https://bag-website.onrender.com/register", {
        name: this.name,
        email: this.email,
        phone: this.phone,
        address: this.address,
        password: this.password
      })
      .then(res => {
        alert("Registration successful!")
        this.$router.push({ name: 'Login' })
      })
      .catch(err => {
        if (err.response && err.response.status === 409) {
          alert("Email already registered.")
        } else {
          alert("Registration failed.")
        }
      })
    }
  }
}
</script>
