<template>
  <v-container>
    <h2 class="text-center mb-4">Shop Our Products</h2>
    <v-row>
      <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <ProductCard :product="product" @add-to-cart="handleAddToCart" />
      </v-col>
    </v-row>
  </v-container>
</template>

<!-- <script>
import axios from 'axios'
import ProductCard from '@/components/shop/ProductCard.vue'

export default {
  name: 'ProductGrid',
  components: { ProductCard },
  data() {
    return {
      products: []
    }
  },
  mounted() {
    axios.get("http://127.0.0.1:5000/products")
      .then(res => {
        this.products = res.data
      })
      .catch(err => console.error(err))
  },
  methods: {
    handleAddToCart(product) {
      alert(`Added ${product.name} to cart!`)
    },

    handleAddToCart(product) {
        let cart = localStorage.getItem('cart')
        cart = cart ? JSON.parse(cart) : []

        // check if product already exists
        const existing = cart.find(item => item.product.id === product.id)
        if (existing) {
        existing.quantity += 1
        } else {
        cart.push({ product, quantity: 1 })
        }

        localStorage.setItem('cart', JSON.stringify(cart))
        alert(`${product.name} added to cart!`)
    }
  }
}
</script> -->
<script>
import axios from 'axios'
import ProductCard from '@/components/shop/ProductCard.vue'

export default {
  name: 'ProductGrid',
  components: { ProductCard },
  data() {
    return {
      products: [],
      allProducts: []
    }
  },
  mounted() {
    axios.get("http://127.0.0.1:5000/products")
      .then(res => {
        this.allProducts = res.data
        this.filterProducts()
      })
      .catch(err => console.error(err))
  },
  watch: {
    '$route.query.category': 'filterProducts'
  },
  methods: {
    filterProducts() {
      const category = this.$route.query.category
      if (category) {
        this.products = this.allProducts.filter(p => p.category === category)
      } else {
        this.products = this.allProducts
      }
    },
    handleAddToCart(product) {
      let cart = localStorage.getItem('cart')
      cart = cart ? JSON.parse(cart) : []

      const existing = cart.find(item => item.product.id === product.id)
      if (existing) {
        existing.quantity += 1
      } else {
        cart.push({ product, quantity: 1 })
      }

      localStorage.setItem('cart', JSON.stringify(cart))
      alert(`${product.name} added to cart!`)
    }
  }
}
</script>

