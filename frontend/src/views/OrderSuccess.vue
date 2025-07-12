<!-- <template>
  <v-container class="text-center">
    <v-icon color="green" size="80">mdi-check-circle</v-icon>
    <h2 class="my-4">Order Placed Successfully!</h2>
    <p>Your order ID is <strong>#{{ orderId }}</strong>.</p>

    <v-btn color="primary" class="mt-4" @click="$router.push({ name: 'Home' })">
      Continue Shopping
    </v-btn>

    <v-btn text class="mt-2" @click="$router.push({ name: 'Myorders' })">
      View My Orders
    </v-btn>
  </v-container>
</template>

<script>
export default {
  name: 'OrderConfirmation',
  props: ['orderId']
}
</script> -->


<template>
  <v-container class="text-center">
    <v-icon color="green" size="100">mdi-check-circle-outline</v-icon>
    <h1 class="my-4">Order Placed Successfully!</h1>
    <h3>Your order ID is: <strong>#{{ orderId }}</strong></h3>

    <v-btn color="primary" class="mt-6" @click="$router.push({ name: 'Home' })">
      Back to Home
    </v-btn>

    <v-btn color="secondary" class="mt-2" @click="$router.push({ name: 'OrderHistory' })">
      View Order History
    </v-btn>
  </v-container>
</template>

<script>
export default {
  name: 'OrderSuccess',
  computed: {
    orderId() {
      return this.$route.params.orderId
    }
  }
}
</script>

<style scoped>
h1 {
  color: #4CAF50;
}
</style>
