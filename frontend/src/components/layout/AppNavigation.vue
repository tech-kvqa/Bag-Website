<!-- <template>
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

    <v-btn text :to="{ name: 'About' }">About</v-btn>
    <v-btn text :to="{ name: 'Contact' }">Contact</v-btn>
    <v-btn text :to="{ name: 'Warranty' }">Warranty</v-btn>
    <v-btn text :to="{ name: 'FAQs' }">FAQs</v-btn>
    <v-btn text :to="{ name: 'Wishlist' }">Wishlist</v-btn>
    <v-btn text :to="{ name: 'Login' }">Login</v-btn>
    <v-btn text :to="{ name: 'Register' }">Register</v-btn>
    <v-btn text :to="{ name: 'Myorders' }">My Orders</v-btn>
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
</script> -->


<!-- <template>
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

    <v-btn text :to="{ name: 'About' }">About</v-btn>
    <v-btn text :to="{ name: 'Contact' }">Contact</v-btn>
    <v-btn text :to="{ name: 'Warranty' }">Warranty</v-btn>
    <v-btn text :to="{ name: 'FAQs' }">FAQs</v-btn>

    <v-btn v-if="loggedIn" text :to="{ name: 'Wishlist' }">Wishlist</v-btn>
    <v-btn v-if="loggedIn" text :to="{ name: 'Myorders' }">My Orders</v-btn>
    <v-btn v-if="loggedIn" text :to="{ name: 'UserDashboard' }">My Dashboard</v-btn>
    <v-btn v-if="loggedIn || adminLoggedIn" text @click="logout">Logout</v-btn> -->

    <!-- <v-btn v-if="!loggedIn" text :to="{ name: 'Login' }">Login</v-btn> -->
      <!-- <v-menu offset-y>
        <template #activator="{ props }">
          <v-btn text v-bind="props">Login</v-btn>
        </template>
        <v-list>
          <v-list-item :to="{ name: 'Login' }">
            <v-list-item-title>User Login</v-list-item-title>
          </v-list-item>
          <v-list-item :to="{ name: 'AdminLogin' }">
            <v-list-item-title>Admin Login</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

    <v-btn v-if="!loggedIn" text :to="{ name: 'Register' }">Register</v-btn>

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
      loggedIn: false,
      adminLoggedIn: false
    }
  },
  mounted() {
    this.checkAuth()
    this.polling = setInterval(this.checkAuth, 1000)
  },
  beforeUnmount() {
    clearInterval(this.polling)
  },
  methods: {
    checkAuth() {
      this.loggedIn = !!localStorage.getItem('user')
      this.adminLoggedIn = !!localStorage.getItem('admin')
    },
    logout() {
      localStorage.removeItem('user')
      this.loggedIn = false
      this.$router.push({ name: 'Home' })
    }
  }
}
</script> -->


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

    <v-btn text :to="{ name: 'About' }">About</v-btn>
    <v-btn text :to="{ name: 'Contact' }">Contact</v-btn>
    <v-btn text :to="{ name: 'Warranty' }">Warranty</v-btn>
    <v-btn text :to="{ name: 'FAQs' }">FAQs</v-btn>

    <!-- User Navigation -->
    <v-btn v-if="loggedIn" text :to="{ name: 'Wishlist' }">Wishlist</v-btn>
    <v-btn v-if="loggedIn" text :to="{ name: 'Myorders' }">My Orders</v-btn>
    <v-btn v-if="loggedIn" text :to="{ name: 'UserDashboard' }">My Dashboard</v-btn>

    <!-- Admin Navigation -->
    <v-btn v-if="adminLoggedIn" text :to="{ name: 'AdminDashboard' }">Admin Dashboard</v-btn>

    <!-- Logout (shown if either user or admin is logged in) -->
    <v-btn v-if="loggedIn || adminLoggedIn" text @click="logout">Logout</v-btn>

    <!-- Login Dropdown (only if no one is logged in) -->
    <v-menu v-if="!loggedIn && !adminLoggedIn" offset-y>
      <template #activator="{ props }">
        <v-btn text v-bind="props">Login</v-btn>
      </template>
      <v-list>
        <v-list-item router :to="{ name: 'Login' }">
          <v-list-item-title>User Login</v-list-item-title>
        </v-list-item>
        <v-list-item router :to="{ name: 'AdminLogin' }">
          <v-list-item-title>Admin Login</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- Register (only for users) -->
    <v-btn v-if="!loggedIn && !adminLoggedIn" text :to="{ name: 'Register' }">Register</v-btn>

    <!-- Cart Icon (only for users) -->
    <v-btn v-if="loggedIn" icon :to="{ name: 'ShoppingCart' }">
      <v-icon>mdi-cart</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppNavigation',
  data() {
    return {
      loggedIn: false,
      adminLoggedIn: false,
      polling: null
    }
  },
  mounted() {
    this.checkAuth()
    this.polling = setInterval(this.checkAuth, 1000)
  },
  beforeUnmount() {
    clearInterval(this.polling)
  },
  methods: {
    checkAuth() {
      this.loggedIn = !!localStorage.getItem('user')
      this.adminLoggedIn = !!localStorage.getItem('admin')
    },
    logout() {
      localStorage.removeItem('user')
      localStorage.removeItem('admin')
      this.loggedIn = false
      this.adminLoggedIn = false
      this.$router.push({ name: 'Home' })
    }
  }
}
</script>

