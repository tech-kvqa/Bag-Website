<!-- <template>
  <v-container>
    <h2 class="mb-4">My Wishlist</h2>
    <v-row>
      <v-col v-for="product in wishlist" :key="product.id" cols="12" sm="6" md="4">
        <ProductCard :product="product" @add-to-cart="addToCart"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import ProductCard from '@/components/shop/ProductCard.vue'
import api from '@/utils/api'

export default {
  name: 'Wishlist',
  components: { ProductCard },
  data() {
    return {
      wishlist: []
    }
  },
  mounted() {
    this.loadWishlist()
  },
  methods: {
    loadWishlist() {
      const user = localStorage.getItem('user')
      if (user) {
        const userId = JSON.parse(user).id
        // axios.get(`http://127.0.0.1:5000/wishlist?user_id=${userId}`)
        api.get(`/wishlist?user_id=${userId}`)
          .then(res => {
            this.wishlist = res.data
          })
          .catch(err => console.error(err))
      }
    },
    addToCart(product) {
      // Existing cart code here
    }
  }
}
</script> -->


<template>
  <v-container>
    <h2 class="mb-4">My Wishlist</h2>

    <v-alert type="info" v-if="wishlist.length === 0">
      No items in your wishlist.
    </v-alert>

    <v-row>
      <v-col v-for="product in wishlist" :key="product.id" cols="12" sm="6" md="4">
        <v-card>
          <v-img :src="getImageUrl(product.image_url)" height="250px"></v-img>
          <v-card-title>{{ product.name }}</v-card-title>
          <v-card-subtitle>₹ {{ product.price }}</v-card-subtitle>
          <v-card-text>{{ product.description }}</v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="addToCart(product)">Add to Cart</v-btn>
            <v-btn color="error" @click="removeFromWishlist(product.id)">Remove</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '@/utils/api'
import { BACKEND_URL } from '@/utils/config'

export default {
  name: 'Wishlist',
  data() {
    return {
      wishlist: []
    }
  },
  mounted() {
    this.loadWishlist()
  },
  methods: {
    getImageUrl(imagePath) {
      return `${BACKEND_URL}${imagePath}`
    },
    loadWishlist() {
      const user = localStorage.getItem('user')
      if (user) {
        const userId = JSON.parse(user).id
        api.get(`/wishlist?user_id=${userId}`)
          .then(res => {
            this.wishlist = res.data
          })
          .catch(err => console.error(err))
      } else {
        this.$router.push('/login')
      }
    },
    addToCart(product) {
      const user = JSON.parse(localStorage.getItem('user'))
      if (user) {
        api.post(`/cart/add`, {
          user_id: user.id,
          product_id: product.id,
          quantity: 1
        })
        .then(() => {
          alert(`${product.name} added to cart!`)
        })
        .catch(err => {
          console.error(err)
          alert('Failed to add to cart')
        })
      } else {
        this.$router.push('/login')
      }
    },
    removeFromWishlist(productId) {
      const user = JSON.parse(localStorage.getItem('user'))
      if (user) {
        api.delete(`/wishlist/delete`, {
          params: {
            user_id: user.id,
            product_id: productId
          }
        })
        .then(() => {
          this.loadWishlist()
          alert('Removed from wishlist')
        })
        .catch(err => console.error(err))
      }
    }
  }
}
</script>
