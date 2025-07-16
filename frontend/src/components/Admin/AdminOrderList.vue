<template>
  <v-container>
    <h2>Manage Orders</h2>

    <v-data-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer</th>
          <th>Total (₹)</th>
          <th>Status</th>
          <th>Date</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.customer_name }}</td>
          <td>{{ order.total_amount }}</td>
          <td>{{ order.status }}</td>
          <td>{{ order.created_on }}</td>
          <td>
            <v-btn small color="success" class="mx-1" @click="previewInvoice(order.id)">
              Invoice
            </v-btn>
            <v-btn small color="info" class="mx-1" @click="viewOrder(order)">
              Details
            </v-btn>

            <v-select
              v-model="order.status"
              :items="['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']"
              dense
              outlined
              class="mt-2"
              @change="updateStatus(order)"
              label="Order Status"
            ></v-select>

            <v-select
              v-model="order.tracking_status"
              :items="['Processed', 'Out for Delivery']"
              dense
              outlined
              class="mt-2"
              label="Tracking Status"
              @change="updateStatus(order)"
            ></v-select>

            <v-text-field
              v-model="order.tracking_id"
              dense
              outlined
              class="mt-2"
              label="Tracking ID"
              @change="updateStatus(order)"
            ></v-text-field>
            <v-btn small color="primary" class="mt-2" @click="updateStatus(order)">
              Save
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-data-table>

    <!-- Order Details Dialog -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>Order #{{ selectedOrder.id }} Details</v-card-title>
        <v-card-text>
          <div v-for="(item, index) in selectedOrder.items" :key="index">
            <p>{{ item.product_name }} (x{{ item.quantity }}) — ₹ {{ item.price * item.quantity }}</p>
          </div>
          <v-divider class="my-2"></v-divider>
          <p><strong>Total:</strong> ₹ {{ selectedOrder.total_amount }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="primary" @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="invoiceDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6">Invoice Preview - Order #{{ selectedInvoiceOrderId }}</v-card-title>
        <v-card-text>
          <iframe
            v-if="selectedInvoiceOrderId"
            :src="getInvoiceUrl(selectedInvoiceOrderId)"
            width="100%"
            height="500px"
            frameborder="0"
          ></iframe>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="downloadInvoice(selectedInvoiceOrderId)">Download</v-btn>
          <v-btn text color="error" @click="invoiceDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AdminOrderList',
  data() {
    return {
      orders: [],
      dialog: false,
      selectedOrder: {},
      invoiceDialog: false,
      selectedInvoiceOrderId: null,
    }
  },
  mounted() {
    this.loadOrders()
  },
  methods: {
    loadOrders() {
      api.get('/admin/orders')
        .then(res => {
          this.orders = res.data
        })
        .catch(err => console.error(err))
    },
    viewOrder(order) {
      this.selectedOrder = order
      this.dialog = true
    },
    updateStatus(order) {
      api.put(`/admin/orders/${order.id}`, {
        status: order.status,
        tracking_status: order.tracking_status,
        tracking_id: order.tracking_id
      })
        .then(() => {
          alert(`Order #${order.id} updated.`)
        })
        .catch(err => console.error(err))
    },
    previewInvoice(orderId) {
      this.selectedInvoiceOrderId = orderId
      this.invoiceDialog = true
    },

    getInvoiceUrl(orderId) {
      return `https://bag-website.onrender.com/admin/order/${orderId}/invoice?preview=true`
    },

    downloadInvoice(orderId) {
      const downloadUrl = `https://bag-website.onrender.com/admin/order/${orderId}/invoice`
      window.open(downloadUrl, '_blank')
    },

    updateStatus(order) {
      api.put(`/admin/orders/${order.id}`, {
        status: order.status,
        tracking_status: order.tracking_status,
        tracking_id: order.tracking_id
      })
        .then(() => {
          alert(`Order #${order.id} updated.`)
        })
        .catch(err => console.error(err))
    }
  }
}
</script>
