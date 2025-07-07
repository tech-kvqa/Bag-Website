<template>
  <v-container>
    <h2 class="mb-4">Checkout</h2>
    <v-row>
      <!-- Order Summary -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Order Summary</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(item, i) in cart" :key="i">
                <v-list-item-content>
                  <v-list-item-title>{{ item.product.name }} (x{{ item.quantity }})</v-list-item-title>
                </v-list-item-content>
                <v-list-item-action>
                  ₹ {{ item.product.price * item.quantity }}
                </v-list-item-action>
              </v-list-item>
            </v-list>
            <v-divider class="my-2"></v-divider>
            <div><strong>Total: ₹ {{ cartTotal }}</strong></div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- User Details -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Delivery Details</v-card-title>
          <v-card-text>
            <v-text-field v-model="customer.name" label="Full Name" outlined></v-text-field>
            <v-text-field v-model="customer.email" label="Email" outlined></v-text-field>
            <v-text-field v-model="customer.phone" label="Phone Number" outlined></v-text-field>
            <v-textarea v-model="customer.address" label="Full Address" outlined></v-textarea>

            <v-radio-group v-model="paymentMethod" label="Payment Method">
              <v-radio label="Cash on Delivery" value="COD"></v-radio>
              <v-radio label="Online Payment" value="Online"></v-radio>
            </v-radio-group>
          </v-card-text>

          <v-card-actions>
            <v-btn color="primary" block @click="placeOrder">Place Order</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Checkout',
  data() {
    return {
      cart: [],
      customer: {
        name: '',
        email: '',
        phone: '',
        address: ''
      },
      paymentMethod: 'COD'
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
    placeOrder() {
      if (!this.customer.name || !this.customer.phone || !this.customer.address) {
        alert("Please fill in all customer details.")
        return
      }
      const orderData = {
        customer_name: this.customer.name,
        email: this.customer.email,
        phone: this.customer.phone,
        address: this.customer.address,
        payment_method: this.paymentMethod,
        total_amount: this.cartTotal,
        cart: this.cart
      }

        // axios.post("http://127.0.0.1:5000/place-order", orderData)
        axios.post("https://bag-website.onrender.com/place-order", orderData)
        .then(res => {
            alert(`Order placed successfully! Order ID: ${res.data.order_id}`)
            localStorage.removeItem('cart')
            this.$router.push({ name: 'Home' })
        })
        .catch(err => {
            console.error(err)
            alert("Error placing order.")
        })
    }
  }
}
</script>
