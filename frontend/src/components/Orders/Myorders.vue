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
        <v-btn size="small" color="primary" class="ml-4" @click="openInvoice(order.order_id)">
          View Invoice
        </v-btn>
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
        <div class="mt-2" v-if="order.tracking_status">
          <strong>Delivery Status:</strong> {{ order.tracking_status }}
        </div>

        <div v-if="order.tracking_id">
          <strong>Tracking ID:</strong> {{ order.tracking_id }}
        </div>
      </v-card-text>
    </v-card>
    <v-dialog v-model="invoiceDialog" max-width="800">
      <v-card>
        <v-card-title>Invoice Preview</v-card-title>
        <v-card-text>
          <iframe :src="invoiceUrl" width="100%" height="500px" frameborder="0"></iframe>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="green" :href="invoiceDownloadUrl" target="_blank" download>Download PDF</v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="invoiceDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import api from '@/utils/api'
import { BACKEND_URL } from '@/utils/config'

export default {
  name: 'MyOrders',
  data() {
    return {
      orders: [],
      user: null,
      invoiceDialog: false,
      invoiceUrl: '',
      invoiceDownloadUrl: ''
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
    },
    openInvoice(orderId) {
      this.invoiceUrl = `${BACKEND_URL}/admin/order/${orderId}/invoice?preview=true`
      this.invoiceDownloadUrl = `${BACKEND_URL}/admin/order/${orderId}/invoice`
      this.invoiceDialog = true
    },
    downloadInvoice() {
      const downloadUrl = `https://bag-website.onrender.com/admin/order/${orderId}/invoice`
      window.open(downloadUrl, '_blank')
    }
  }
}
</script>
