<template>
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
        axios.get(`http://127.0.0.1:5000/wishlist?user_id=${userId}`)
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
</script>
