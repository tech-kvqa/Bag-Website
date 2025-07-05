<!-- <template>
  <v-container>
    <h2>Your Shopping Cart</h2>
    <v-divider class="mb-4"></v-divider>

    <v-alert v-if="cart.length === 0" type="info" outlined>
      Your cart is empty.
    </v-alert>

    <v-row v-else>
      <v-col cols="12" md="8">
        <v-card v-for="(item, index) in cart" :key="index" class="mb-4">
          <v-row>
            <v-col cols="4">
              <v-img :src="item.product.image_url" height="150px"></v-img>
            </v-col>
            <v-col cols="8">
              <v-card-title>{{ item.product.name }}</v-card-title>
              <v-card-subtitle>₹ {{ item.product.price }}</v-card-subtitle>
              <v-text-field
                v-model="item.quantity"
                type="number"
                label="Quantity"
                min="1"
                @change="updateCart"
              />
              <v-btn color="error" @click="removeFromCart(index)">Remove</v-btn>
              <v-btn color="primary" block :to="{ name: 'Checkout' }">Proceed to Checkout</v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Cart Summary</v-card-title>
          <v-card-text>
            <div>Subtotal: ₹ {{ cartTotal }}</div>
            <v-divider class="my-2"></v-divider>
            <v-btn color="primary" block>Proceed to Checkout</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ShoppingCart',
  data() {
    return {
      cart: []
    }
  },
  computed: {
    cartTotal() {
      return this.cart.reduce((total, item) => {
        return total + (item.product.price * item.quantity)
      }, 0)
    }
  },
  mounted() {
    this.loadCart()
  },
  methods: {
    loadCart() {
      const storedCart = localStorage.getItem('cart')
      this.cart = storedCart ? JSON.parse(storedCart) : []
    },
    updateCart() {
      localStorage.setItem('cart', JSON.stringify(this.cart))
    },
    removeFromCart(index) {
      this.cart.splice(index, 1)
      this.updateCart()
    }
  }
}
</script> -->


<template>
  <v-container>
    <h2 class="mb-4">Your Shopping Cart</h2>

    <v-alert v-if="cartItems.length === 0" type="info">
      Your cart is empty.
    </v-alert>

    <v-row v-else>
      <v-col v-for="(item, index) in cartItems" :key="index" cols="12" sm="6" md="4">
        <v-card>
          <v-img :src="item.product.image_url" height="200px"></v-img>
          <v-card-title>{{ item.product.name }}</v-card-title>
          <v-card-subtitle>₹ {{ item.product.price }}</v-card-subtitle>

          <v-card-text>
            <div>
              <strong>Quantity:</strong>
              <v-btn icon @click="decreaseQuantity(item)"><v-icon>mdi-minus</v-icon></v-btn>
              {{ item.quantity }}
              <v-btn icon @click="increaseQuantity(item)"><v-icon>mdi-plus</v-icon></v-btn>
            </div>
            <div class="mt-2">
              <strong>Total: ₹ {{ item.product.price * item.quantity }}</strong>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn color="error" @click="removeItem(item)">Remove</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <v-card v-if="cartItems.length > 0" class="pa-4">
      <h3>Total Amount: ₹ {{ cartTotal }}</h3>
      <v-btn color="primary" @click="checkout">Proceed to Checkout</v-btn>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ShoppingCart',
  data() {
    return {
      cartItems: [],
      user: null
    }
  },
  mounted() {
    this.user = JSON.parse(localStorage.getItem('user'))
    this.loadCart()
  },
  computed: {
    cartTotal() {
      return this.cartItems.reduce((total, item) => total + item.product.price * item.quantity, 0)
    }
  },
  methods: {
    loadCart() {
      if (this.user) {
        // Load cart from server
        axios.get(`http://127.0.0.1:5000/cart?user_id=${this.user.id}`)
          .then(res => {
            this.cartItems = res.data
          })
          .catch(err => console.error(err))
      } else {
        // Load cart from localStorage
        const localCart = JSON.parse(localStorage.getItem('cart') || '[]')
        this.cartItems = localCart
      }
    },
    increaseQuantity(item) {
      item.quantity += 1
      this.updateCart(item)
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity -= 1
        this.updateCart(item)
      }
    },
    updateCart(item) {
      if (this.user) {
        // Update server-side cart
        axios.post('http://127.0.0.1:5000/cart', {
          user_id: this.user.id,
          product_id: item.product.id,
          quantity: 1
        })
        .then(() => this.loadCart())
        .catch(err => console.error(err))
      } else {
        // Update localStorage cart
        let cart = JSON.parse(localStorage.getItem('cart') || '[]')
        const existing = cart.find(c => c.product.id === item.product.id)
        if (existing) {
          existing.quantity = item.quantity
        }
        localStorage.setItem('cart', JSON.stringify(cart))
      }
    },
    removeItem(item) {
      if (this.user) {
        // Remove from server cart
        axios.delete(`http://127.0.0.1:5000/cart/clear?user_id=${this.user.id}`)
          .then(() => this.loadCart())
          .catch(err => console.error(err))
      } else {
        // Remove from localStorage cart
        let cart = JSON.parse(localStorage.getItem('cart') || '[]')
        cart = cart.filter(c => c.product.id !== item.product.id)
        localStorage.setItem('cart', JSON.stringify(cart))
        this.loadCart()
      }
    },
    checkout() {
      alert("Proceeding to checkout functionality will be implemented in Phase 12")
    }
  }
}
</script>
