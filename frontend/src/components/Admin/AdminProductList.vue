<template>
  <v-container>
    <h2>Manage Products</h2>
    <v-btn color="primary" class="mb-4" @click="$router.push({ name: 'AddProduct' })">Add New Product</v-btn>

    <v-simple-table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.name }}</td>
          <td>{{ product.category }}</td>
          <td>₹ {{ product.price }}</td>
          <td>
            <v-btn small color="primary" @click="editProduct(product.id)">Edit</v-btn>
            <v-btn small color="error" @click="deleteProduct(product.id)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AdminProductList',
  data() {
    return {
      products: []
    }
  },
  mounted() {
    this.loadProducts()
  },
  methods: {
    loadProducts() {
      api.get('/admin/products')
        .then(res => {
          this.products = res.data
        })
        .catch(err => console.error(err))
    },
    editProduct(id) {
      this.$router.push({ name: 'EditProduct', params: { id } })
    },
    deleteProduct(id) {
      if (confirm('Are you sure you want to delete this product?')) {
        api.delete(`/admin/products/${id}`)
          .then(() => this.loadProducts())
          .catch(err => console.error(err))
      }
    }
  }
}
</script>
