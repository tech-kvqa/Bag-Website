<template>
  <v-container>
    <h2 class="mb-4">My Orders</h2>

    <v-alert type="info" v-if="orders.length === 0">
      You have no past orders yet.
    </v-alert>

    <v-card v-for="order in orders" :key="order.order_id" class="mb-4">
      <v-card-title>
        <strong>Order #{{ order.order_id }}</strong>
        <v-spacer></v-spacer>
        <span>Status: <strong class="ml-2">{{ order.status }}</strong></span>
      </v-card-title>

      <v-card-text>
        <v-list dense>
          <v-list-item v-for="(item, idx) in order.items" :key="idx">
            <v-list-item-content>
              {{ item.product_name }} x {{ item.quantity }}
            </v-list-item-content>
            <v-list-item-content class="text-right">
              ₹ {{ item.price * item.quantity }}
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-divider class="my-2"></v-divider>
        <div><strong>Total: ₹ {{ order.total_amount }}</strong></div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'MyOrders',
  data() {
    return {
      orders: [],
      user: null
    }
  },
  mounted() {
    this.user = JSON.parse(localStorage.getItem('user'))
    if (this.user) {
      this.fetchOrders()
    }
  },
  methods: {
    fetchOrders() {
      api.get(`/order-history/${this.user.id}`)
        .then(res => {
          this.orders = res.data
        })
        .catch(err => console.error(err))
    }
  }
}
</script>
