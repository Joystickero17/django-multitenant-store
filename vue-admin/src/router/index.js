import Vue from 'vue'
import VueRouter from 'vue-router'
import DashboardVue from '../views/Dashboard.vue'
import ContactosView from '@/views/ContactosView.vue'
import ProductosView from '@/views/ProductosView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import ProductEditView from '@/views/ProductEditView.vue'

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
    meta:{verbose_name:"Productos"},       
  },
  {
    path: '/products/detail/:id',
    name:"product.detail",
    component: ProductDetailView,
    meta:{verbose_name:"Detalles del Producto"},    
  },
  {
    path: '/products/edit/:id',
    name:"product.edit",
    component: ProductEditView,
    meta:{verbose_name:"Editar Producto"},    
  },
]

const router = new VueRouter({
  routes,
  mode: "history",
  base:"/store-admin/"
})

export default router
