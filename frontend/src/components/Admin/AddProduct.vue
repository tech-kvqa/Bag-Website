<template>
  <v-container>
    <h1 class="mb-4">Add New Product</h1>

    <v-form ref="form" @submit.prevent="addProduct">

      <v-text-field v-model="product.name" label="Product Name" outlined required></v-text-field>

      <v-textarea v-model="product.description" label="Description" outlined required></v-textarea>

      <v-text-field v-model="product.price" label="Price (₹)" type="number" outlined required></v-text-field>

      <v-text-field v-model="product.stock" label="Stock Quantity" type="number" outlined required></v-text-field>

      <v-select
        v-model="product.category"
        :items="categories"
        label="Category"
        outlined
        required
      ></v-select>

      <!-- Image upload -->
      <v-file-input
        v-model="productImage"
        label="Product Image"
        accept="image/*"
        outlined
        required
        prepend-icon="mdi-camera"
      ></v-file-input>

      <v-btn color="primary" type="submit" class="mt-4">Add Product</v-btn>
      <v-btn text class="mt-4" @click="$router.push({ name: 'AdminProductList' })">Back to Product List</v-btn>

    </v-form>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AddProduct',
  data() {
    return {
      product: {
        name: '',
        description: '',
        price: null,
        stock: null,
        category: ''
      },
      productImage: null,
      categories: ['Backpacks', 'School Bags', 'Luggage', 'Accessories']
    }
  },
  methods: {
    addProduct() {
      if (!this.product.name || !this.product.price || !this.product.stock || !this.product.category || !this.productImage) {
        alert('Please fill in all fields.')
        return
      }

      const formData = new FormData()
      formData.append('name', this.product.name)
      formData.append('description', this.product.description)
      formData.append('price', this.product.price)
      formData.append('stock', this.product.stock)
      formData.append('category', this.product.category)
      formData.append('image', this.productImage)

      api.post('/admin/add-product', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
        .then(() => {
          alert('Product added successfully!')
          this.$router.push({ name: 'AdminProductList' })
        })
        .catch(err => {
          console.error(err)
          alert('Failed to add product.')
        })
    }
  }
}
</script>
