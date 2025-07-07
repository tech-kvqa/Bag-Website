<template>
  <v-container>
    <h2 class="mb-4">My Dashboard</h2>

    <v-card class="mb-4">
      <v-card-title>User Information</v-card-title>
      <v-card-text>
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Phone:</strong> {{ user.phone }}</p>
        <p><strong>Address:</strong> {{ user.address }}</p>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>My Orders</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="order in orders" :key="order.order_id">
            <v-list-item-content>
              <v-list-item-title>Order #{{ order.order_id }} — ₹ {{ order.total_amount }}</v-list-item-title>
              <v-list-item-subtitle>Status: {{ order.status }}</v-list-item-subtitle>
              <v-list dense>
                <v-list-item v-for="(item, i) in order.items" :key="i">
                  <v-list-item-content>
                    {{ item.product_name }} (x{{ item.quantity }}) — ₹ {{ item.price }}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data() {
    return {
      user: {},
      orders: []
    }
  },
  mounted() {
    this.loadUser()
    this.loadOrders()
  },
  methods: {
    loadUser() {
      const user = localStorage.getItem('user')
      this.user = user ? JSON.parse(user) : {}
    },
    loadOrders() {
      const user = localStorage.getItem('user')
      if (user) {
        const userId = JSON.parse(user).id
        // axios.get(`http://127.0.0.1:5000/orders?user_id=${userId}`)
        axios.get(`https://bag-website.onrender.com/orders?user_id=${userId}`)
          .then(res => {
            this.orders = res.data
          })
          .catch(err => console.error(err))
      }
    }
  }
}
</script>
