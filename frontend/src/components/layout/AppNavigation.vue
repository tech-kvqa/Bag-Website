<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title class="font-weight-bold">HotshotBags</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn text :to="{ name: 'Home' }">Home</v-btn>

    <v-menu offset-y>
      <template #activator="{ props }">
        <v-btn text v-bind="props">Shop</v-btn>
      </template>
      <v-list>
        <v-list-item router :to="{ name: 'ProductGrid' }">
          <v-list-item-title>All Products</v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item router :to="{ name: 'ProductGrid', query: { category: 'Backpacks' } }">
          <v-list-item-title>Backpacks</v-list-item-title>
        </v-list-item>
        <v-list-item router :to="{ name: 'ProductGrid', query: { category: 'School Bags' } }">
          <v-list-item-title>School Bags</v-list-item-title>
        </v-list-item>
        <v-list-item router :to="{ name: 'ProductGrid', query: { category: 'Luggage' } }">
          <v-list-item-title>Luggage</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- <v-btn text :to="{ name: 'ShoppingCart' }">Cart</v-btn> -->
    <v-btn text :to="{ name: 'About' }">About</v-btn>
    <v-btn text :to="{ name: 'Contact' }">Contact</v-btn>
    <v-btn text :to="{ name: 'Warranty' }">Warranty</v-btn>
    <v-btn text :to="{ name: 'FAQs' }">FAQs</v-btn>
    <v-btn text :to="{ name: 'Wishlist' }">Wishlist</v-btn>
    <v-btn text :to="{ name: 'Login' }">Login</v-btn>
    <v-btn text :to="{ name: 'Register' }">Register</v-btn>
    <v-btn v-if="loggedIn" text :to="{ name: 'UserDashboard' }">My Dashboard</v-btn>



    <v-btn icon :to="{ name: 'ShoppingCart' }">
      <v-icon>mdi-cart</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppNavigation',
  data() {
    return {
        loggedIn: false
    }
  },
    mounted() {
    this.loggedIn = !!localStorage.getItem('user')
  }
}
</script>
