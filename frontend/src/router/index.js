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
import AdminLogin from '../views/AdminLogin.vue';
import AdminDashboard from '../components/auth/AdminDashboard.vue';
import AdminProductList from '../components/Admin/AdminProductList.vue';
import AddProduct from '../components/Admin/AddProduct.vue';
import EditProduct from '../components/Admin/EditProduct.vue';
import AdminOrderList from '../components/Admin/AdminOrderList.vue';
import AdminUserList from '../components/Admin/AdminUserList.vue';
import LowStockALerts from '../components/Admin/LowStockALerts.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/shop', name: 'ProductGrid', component: ProductGrid },
  { path: '/product/:id', name: 'product-details', component: ProductDetails },
  { path: '/cart', name: 'ShoppingCart', component: ShoppingCart, meta: { requiresAuth: true } },
  { path: '/checkout', name: 'Checkout', component: Checkout, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'UserDashboard', component: UserDashboard },
  { path: '/wishlist', name: 'Wishlist', component: Wishlist, meta: { requiresAuth: true } },
  { path: '/about', name: 'About', component: About },
  { path: '/contact', name: 'Contact', component: Contact },
  { path: '/warranty', name: 'Warranty', component: Warranty },
  { path: '/faqs', name: 'FAQs', component: FAQs },
  { path: '/my-orders', name: 'Myorders', component: Myorders, meta: { requiresAuth: true } },
  {
    path: '/order-success/:orderId',
    name: 'OrderSuccess',
    component: () => import('@/views/OrderSuccess.vue')
  },
  { path: '/admin/login', name: 'AdminLogin', component: AdminLogin },
  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAdmin: true }},
  { path: '/admin/products', name: 'AdminProductList', component: AdminProductList, meta: { requiresAdminAuth: true }},
  { path: '/admin/add-product', name: 'AddProduct', component: AddProduct, meta: { requiresAdminAuth: true }},
  { path: '/admin/edit-product/:id', name: 'EditProduct', component: EditProduct, meta: { requiresAdminAuth: true } },
  { path: '/admin/orders', name: 'AdminOrderList', component: AdminOrderList, meta: { requiresAdmin: true }},
  { path: '/admin/users', name: 'AdminUserList', component: AdminUserList, meta: { requiresAdmin: true } },
  { path: '/admin/low-stock', name: 'LowStockAlerts', component: LowStockALerts, meta: { requiresAdmin: true }},


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('user')
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
