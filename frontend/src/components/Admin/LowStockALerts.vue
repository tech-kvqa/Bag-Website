<template>
  <v-container>
    <h2>Low Stock Alerts</h2>

    <v-alert
      v-if="products.length === 0"
      type="success"
      class="my-4"
      text
    >
      All products are sufficiently stocked.
    </v-alert>

    <v-data-table
      v-else
      :headers="headers"
      :items="products"
      :items-per-page="5"
      class="elevation-1"
    >
      <template #item.stock="{ item }">
        <span class="text-error font-weight-bold">{{ item.stock }}</span>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'LowStockAlerts',
  data() {
    return {
      products: [],
      headers: [
        { title: 'Name', value: 'name' },
        { title: 'Category', value: 'category' },
        { title: 'Price (₹)', value: 'price' },
        { title: 'Stock', value: 'stock' }
      ]
    }
  },
  mounted() {
    api.get('/admin/low-stock-products')
      .then(res => {
        this.products = res.data
      })
      .catch(err => console.error(err))
  }
}
</script>
