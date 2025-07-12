<template>
  <v-container>
    <h2 class="mb-4">Login</h2>
    <v-text-field v-model="email" label="Email" outlined></v-text-field>
    <v-text-field v-model="password" label="Password" type="password" outlined></v-text-field>
    <v-btn color="primary" block @click="login">Login</v-btn>
  </v-container>
</template>

<script>
import axios from 'axios'
import api from '@/utils/api'

export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login() {
      api.post("/login", {
      // axios.post("https://bag-website.onrender.com/login", {
        email: this.email,
        password: this.password
        })
        .then(res => {
        localStorage.setItem('user', JSON.stringify(res.data.user))

        // Sync local cart to server if user logged in
        const cart = JSON.parse(localStorage.getItem('cart') || '[]')
        const userId = res.data.user.id

        cart.forEach(item => {
            // axios.post('http://127.0.0.1:5000/cart', {
            axios.post('https://bag-website.onrender.com/cart', {
            user_id: userId,
            product_id: item.product.id,
            quantity: item.quantity
            })
        })

        // Clear local cart after sync (optional)
        localStorage.removeItem('cart')

        alert("Logged in and cart synced!")
        this.$router.push({ name: 'Home' })
        })
    }
  }
}
</script>
