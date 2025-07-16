<template>
  <v-container>
    <h2>Edit Product</h2>

    <v-form @submit.prevent="updateProduct">
      <v-text-field v-model="product.name" label="Product Name" required></v-text-field>
      <v-textarea v-model="product.description" label="Description" required></v-textarea>
      <v-text-field v-model="product.price" label="Price" type="number" required></v-text-field>
      <v-text-field v-model="product.stock" label="Stock Quantity" type="number" required></v-text-field>
      <v-text-field v-model="product.category" label="Category" required></v-text-field>

      <v-file-input v-model="imageFile" label="Replace Image (optional)" accept="image/*"></v-file-input>

      <v-btn type="submit" color="primary" class="mt-4">Update Product</v-btn>
      <v-btn text class="mt-4" @click="$router.push({ name: 'AdminProductList' })">Cancel</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'EditProduct',
  data() {
    return {
      product: {
        name: '',
        description: '',
        price: '',
        stock: '',
        category: ''
      },
      imageFile: null
    }
  },
  mounted() {
    this.fetchProduct()
  },
  methods: {
    fetchProduct() {
      const id = this.$route.params.id
      api.get(`/admin/products/${id}`)
        .then(res => {
          this.product = res.data
        })
        .catch(err => {
          console.error(err)
          alert('Failed to load product details')
        })
    },
    updateProduct() {
      const id = this.$route.params.id
      const formData = new FormData()
      formData.append('name', this.product.name)
      formData.append('description', this.product.description)
      formData.append('price', this.product.price)
      formData.append('stock', this.product.stock)
      formData.append('category', this.product.category)
      if (this.imageFile) {
        formData.append('image', this.imageFile)
      }

      api.put(`/admin/products/${id}`, formData)
        .then(() => {
          alert('Product updated successfully!')
          this.$router.push({ name: 'AdminProductList' })
        })
        .catch(err => {
          console.error(err)
          alert('Failed to update product')
        })
    }
  }
}
</script>
