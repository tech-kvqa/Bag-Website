<!-- <template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-img :src="product.image_url" height="500px" cover></v-img>
      </v-col>
      <v-col cols="12" md="6">
        <h1>{{ product.name }}</h1>
        <h3>₹ {{ product.price }}</h3>
        <p>{{ product.description }}</p>
        <v-text-field v-model="quantity" type="number" label="Quantity" min="1" class="mt-4"></v-text-field>
        <v-btn color="primary" class="mt-2" @click="addToCart">Add to Cart</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProductDetails',
  data() {
    return {
      product: {},
      quantity: 1
    }
  },
  mounted() {
    const productId = this.$route.params.id
    axios.get(`http://127.0.0.1:5000/products/${productId}`)
      .then(res => {
        this.product = res.data
      })
      .catch(err => console.error(err))
  },
  methods: {
    addToCart() {
      alert(`Added ${this.quantity} ${this.product.name}(s) to cart!`)
    }
  }
}
</script> -->



<!-- <template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-img :src="getImageUrl(product.image_url)" height="500px" cover></v-img>
      </v-col>
      <v-col cols="12" md="6">
        <h1>{{ product.name }}</h1>
        <h3>₹ {{ product.price }}</h3>
        <p>{{ product.description }}</p>
        <v-text-field v-model="quantity" type="number" label="Quantity" min="1" class="mt-4"></v-text-field>
        <v-btn color="primary" class="mt-2" @click="addToCart">Add to Cart</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { BACKEND_URL } from '@/utils/config'

export default {
  name: 'ProductDetails',
  data() {
    return {
      product: {},
      quantity: 1
    }
  },
  mounted() {
    const productId = this.$route.params.id
    axios.get(`${BACKEND_URL}/products/${productId}`)
      .then(res => {
        this.product = res.data
      })
      .catch(err => console.error(err))
  },
  methods: {
    getImageUrl(imagePath) {
      return `${BACKEND_URL}${imagePath}`
    },
    addToCart() {
      alert(`Added ${this.quantity} ${this.product.name}(s) to cart!`)
    }
  }
}
</script> -->


<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-img :src="getImageUrl(product.image_url)" height="500px" cover></v-img>
      </v-col>
      <v-col cols="12" md="6">
        <h1>{{ product.name }}</h1>
        <h3>₹ {{ product.price }}</h3>
        <p>{{ product.description }}</p>
        <v-text-field v-model="quantity" type="number" label="Quantity" min="1" class="mt-4"></v-text-field>
        <v-btn color="primary" class="mt-2" @click="addToCart">Add to Cart</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { BACKEND_URL } from '@/utils/config'
import api from '@/utils/api'

export default {
  name: 'ProductDetails',
  data() {
    return {
      product: {},
      quantity: 1
    }
  },
  mounted() {
    const productId = this.$route.params.id
    axios.get(`${BACKEND_URL}/products/${productId}`)
      .then(res => {
        this.product = res.data
      })
      .catch(err => console.error(err))
  },
  methods: {
    getImageUrl(imagePath) {
      return `${BACKEND_URL}${imagePath}`
    },
    addToCart() {
      const user = JSON.parse(localStorage.getItem('user'))
      if (user) {
        // Logged in — Add to server cart
        api.post(`/cart/add`, {
          user_id: user.id,
          product_id: this.product.id,
          quantity: this.quantity
        })
        .then(() => {
          alert(`${this.quantity} ${this.product.name}(s) added to your cart!`)
        })
        .catch(err => {
          console.error(err)
          alert('Failed to add to cart')
        })
      } else {
        // Guest — Add to localStorage cart
        let cart = JSON.parse(localStorage.getItem('cart') || '[]')
        const existing = cart.find(c => c.product.id === this.product.id)
        if (existing) {
          existing.quantity += parseInt(this.quantity)
        } else {
          cart.push({ product: this.product, quantity: parseInt(this.quantity) })
        }
        localStorage.setItem('cart', JSON.stringify(cart))
        alert(`${this.quantity} ${this.product.name}(s) added to your cart!`)
      }
    }
  }
}
</script>
