import Vue from 'vue'
import VueRouter from 'vue-router'
import DashboardVue from '../views/Dashboard.vue'
import ContactosView from '@/views/ContactosView.vue'
import ProductosView from '@/views/ProductosView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardVue,
    meta:{verbose_name:"Estadisticas"}
  },
  {
    path: '/contacts',
    name: 'contactos-list',
    component: ContactosView,
    meta:{verbose_name:"Contactos"}
        
  },
  {
    path: '/products',
    name: 'productos-list',
    component: ProductosView,
    meta:{verbose_name:"Productos"}
        
  }
]

const router = new VueRouter({
  routes
})

export default router
