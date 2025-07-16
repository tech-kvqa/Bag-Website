<!-- <template>
  <v-card max-width="344" class="mx-auto my-4" outlined>
    <v-img :src="product.image_url" height="200px"></v-img>
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>₹ {{ product.price }}</v-card-subtitle>
    <v-card-text>{{ product.description }}</v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="$emit('add-to-cart', product)">Add to Cart</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ProductCard',
  props: ['product']
}
</script> -->

<!-- 
<template>
  <v-card
    max-width="344"
    class="mx-auto my-4"
    outlined
    :to="{ name: 'product-details', params: { id: product.id } }"
    link
  >
    <v-img :src="product.image_url" height="200px"></v-img>
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>₹ {{ product.price }}</v-card-subtitle>
    <v-card-text>{{ product.description }}</v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click.stop="$emit('add-to-cart', product)">Add to Cart</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ProductCard',
  props: ['product']
}
</script> -->

<template>
  <v-card
    max-width="344"
    class="mx-auto my-4"
    outlined
    :to="{ name: 'product-details', params: { id: product.id } }"
    link
  >
    <v-img :src="getImageUrl(product.image_url)" height="200px"></v-img>
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>₹ {{ product.price }}</v-card-subtitle>
    <v-card-text>{{ product.description }}</v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click.stop="addToCart">Add to Cart</v-btn>
      <v-btn icon color="pink" @click="addToWishlist">
        <v-icon>mdi-heart</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { BACKEND_URL } from '@/utils/config'
import api from '@/utils/api'

export default {
  name: 'ProductCard',
  props: ['product'],
  methods: {
    getImageUrl(imagePath) {
      return `${BACKEND_URL}${imagePath}`
    },
    addToCart() {
      const user = JSON.parse(localStorage.getItem('user'))
      if (user) {
        // logged-in: add to server cart
        api.post('/cart/add', {
          user_id: user.id,
          product_id: this.product.id,
          quantity: 1
        })
        .then(() => {
          this.$emit('cart-updated')
          this.$toast.success('Added to cart!')
        })
        .catch(err => {
          console.error(err)
          this.$toast.error('Error adding to cart')
        })
      } else {
        // guest: add to localStorage cart
        let cart = JSON.parse(localStorage.getItem('cart') || '[]')
        const existing = cart.find(c => c.product.id === this.product.id)
        if (existing) {
          existing.quantity += 1
        } else {
          cart.push({ product: this.product, quantity: 1 })
        }
        localStorage.setItem('cart', JSON.stringify(cart))
        this.$toast.success('Added to cart!')
      }
    },
    addToWishlist() {
      const user = JSON.parse(localStorage.getItem('user'))
      if (user) {
        api.post('/wishlist', {
          user_id: user.id,
          product_id: this.product.id
        })
        .then(() => {
          alert(`${this.product.name} added to wishlist!`)
        })
        .catch(err => {
          console.error(err)
          alert('Failed to add to wishlist')
        })
      } else {
        this.$router.push('/login')
      }
    }
  }
}
</script>

