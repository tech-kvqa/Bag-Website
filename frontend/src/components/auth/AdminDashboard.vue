<!-- <template>
  <v-container>
    <h1>Admin Dashboard</h1>

    <v-row class="mt-6" dense>
      <v-col cols="12" sm="6" md="4">
        <v-card @click="$router.push({ name: 'AdminProductList' })" class="text-center pa-4" hover>
          <v-icon size="50" color="primary">mdi-package-variant</v-icon>
          <h3 class="mt-2">Manage Products</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <v-card @click="$router.push({ name: 'AdminOrderList' })" class="text-center pa-4" hover>
          <v-icon size="50" color="primary">mdi-cart</v-icon>
          <h3 class="mt-2">Manage Orders</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <v-card @click="$router.push({ name: 'AdminUserList' })" class="text-center pa-4" hover>
          <v-icon size="50" color="primary">mdi-account-multiple</v-icon>
          <h3 class="mt-2">Manage Users</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <v-card @click="logout" class="text-center pa-4" hover>
          <v-icon size="50" color="error">mdi-logout</v-icon>
          <h3 class="mt-2">Logout</h3>
        </v-card>
      </v-col>

    </v-row>
  </v-container>
</template>

<script>
export default {
  mounted() {
    if (!localStorage.getItem('admin')) {
      this.$router.push({ name: 'AdminLogin' })
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('admin')
      this.$router.push({ name: 'AdminLogin' })
    }
  }
}
</script> -->


<template>
  <v-container>
    <h1 class="mb-6">Admin Dashboard</h1>

    <v-menu offset-y>
      <template #activator="{ props }">
        <v-btn icon v-bind="props">
          <v-badge :content="unreadCount" color="red" overlap>
            <v-icon>mdi-bell</v-icon>
          </v-badge>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(notif, index) in lowStockNotifications"
          :key="index"
        >
          <v-list-item-title>
            ⚠️ {{ notif.product_name }} stock is low ({{ notif.stock }} left)
          </v-list-item-title>
        </v-list-item>
        <v-list-item @click="markAsRead">
          <v-list-item-title class="text-blue">Mark all as read</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>


    <!-- Stats Summary -->
    <v-row dense class="mb-6">
      <v-col cols="12" sm="4">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon color="primary" size="40">mdi-account-multiple</v-icon>
          <h2>{{ stats.total_users }}</h2>
          <div>Total Users</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon color="green" size="40">mdi-cart</v-icon>
          <h2>{{ stats.total_orders }}</h2>
          <div>Total Orders</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card elevation="2" class="text-center pa-4">
          <v-icon color="blue" size="40">mdi-package-variant</v-icon>
          <h2>{{ stats.total_products }}</h2>
          <div>Total Products</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Navigation Cards -->
    <v-row dense>
      <v-col cols="12" sm="6" md="3">
        <v-card @click="$router.push({ name: 'AdminProductList' })" class="text-center pa-4 dashboard-card" hover>
          <v-icon size="50" color="blue">mdi-package-variant</v-icon>
          <h3 class="mt-2">Manage Products</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card @click="$router.push({ name: 'AdminOrderList' })" class="text-center pa-4 dashboard-card" hover>
          <v-icon size="50" color="green">mdi-cart</v-icon>
          <h3 class="mt-2">Manage Orders</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card @click="$router.push({ name: 'AdminUserList' })" class="text-center pa-4 dashboard-card" hover>
          <v-icon size="50" color="purple">mdi-account-multiple</v-icon>
          <h3 class="mt-2">Manage Users</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <v-card @click="$router.push({ name: 'LowStockAlerts' })" class="text-center pa-4" hover>
          <v-icon size="50" color="orange">mdi-alert-box</v-icon>
          <h3 class="mt-2">Inventory Alerts</h3>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card @click="logout" class="text-center pa-4 dashboard-card" hover>
          <v-icon size="50" color="red">mdi-logout</v-icon>
          <h3 class="mt-2">Logout</h3>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '@/utils/api'
import { io } from "socket.io-client"

export default {
  data() {
    return {
      stats: {
        total_users: 0,
        total_orders: 0,
        total_products: 0
      },
      socket: null,
      lowStockNotifications: [],
      unreadCount: 0
    }
  },
  mounted() {
    this.socket = io("https://bag-website.onrender.com")

    this.socket.on("low_stock_alert", (data) => {
      this.lowStockNotifications.push(data)
      this.unreadCount++
    })

    if (!localStorage.getItem('admin')) {
      this.$router.push({ name: 'AdminLogin' })
    } else {
      this.loadStats()
      this.loadUnreadNotifications()
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('admin')
      this.$router.push({ name: 'AdminLogin' })
    },
    loadStats() {
      api.get('/admin/stats')
        .then(res => {
          this.stats = res.data
        })
        .catch(err => {
          console.error('Failed to fetch stats:', err)
        })
    },
    markAsRead() {
      this.unreadCount = 0
      api.post('/admin/notifications/read')  // ← use imported `api`, not `this.$axios`
        .catch(err => console.error('Failed to mark notifications as read:', err))
    },
    loadUnreadNotifications() {
      api.get('/admin/notifications')
        .then(res => {
          this.lowStockNotifications = res.data.map(n => ({
            product_name: this.extractProductName(n.message),
            stock: this.extractStockCount(n.message)
          }))
          this.unreadCount = res.data.length
        })
        .catch(err => {
          console.error('Failed to fetch notifications', err)
        })
    },
    extractProductName(message) {
      const match = message.match(/'(.+?)'/)
      return match ? match[1] : 'Unknown'
    },
    extractStockCount(message) {
      const match = message.match(/only (\d+) left/)
      return match ? parseInt(match[1]) : 0
    }
  }
}
</script>

<style scoped>
.dashboard-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}
.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}
</style>
