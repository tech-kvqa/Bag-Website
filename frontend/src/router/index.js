import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue';
import ProductGrid from '../components/shop/ProductGrid.vue';
import ProductDetails from '../components/shop/ProductDetails.vue';
import ShoppingCart from '../components/shop/ShoppingCart.vue';
import Checkout from '../components/shop/Checkout.vue';
import Login from '../views/Login.vue';
import Register from  '../views/Register.vue';
import Wishlist from '../components/shop/WishList.vue';
import UserDashboard from '../components/auth/UserDashboard.vue';
import About from '../views/About.vue';
import Contact from '../views/Contact.vue';
import Warranty from '../views/Warranty.vue';
import FAQs from '../views/FAQs.vue';
import Myorders from '../components/Orders/Myorders.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/shop', name: 'ProductGrid', component: ProductGrid },
  { path: '/product/:id', name: 'product-details', component: ProductDetails },
  { path: '/cart', name: 'ShoppingCart', component: ShoppingCart },
  { path: '/checkout', name: 'Checkout', component: Checkout },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'UserDashboard', component: UserDashboard },
  { path: '/wishlist', name: 'Wishlist', component: Wishlist },
  { path: '/about', name: 'About', component: About },
  { path: '/contact', name: 'Contact', component: Contact },
  { path: '/warranty', name: 'Warranty', component: Warranty },
  { path: '/faqs', name: 'FAQs', component: FAQs },
  { path: '/my-orders', name: 'Myorders', component: Myorders },
  {
    path: '/order-success/:orderId',
    name: 'OrderSuccess',
    component: () => import('@/views/OrderSuccess.vue')
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
