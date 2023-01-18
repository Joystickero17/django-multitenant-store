import Vue from 'vue'
import VueRouter from 'vue-router'
import DashboardVue from '../views/Dashboard.vue'
import ContactosView from '@/views/ContactosView.vue'
import ProductosView from '@/views/ProductosView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import ProductEditView from '@/views/ProductEditView.vue'
import ProductNewView from '@/views/ProductNewView.vue'
import VentasViewVue from '@/views/VentasView.vue'
import VentasDetailViewVue from '@/views/VentasDetailView.vue'

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
    path: '/ventas',
    name: 'ventas-list',
    component: VentasViewVue,
    meta:{verbose_name:"Ventas"}
        
  },
  {
    path: '/ventas/detail/:id',
    name: 'ventas.detail',
    component: VentasDetailViewVue,
    meta:{verbose_name:"Detalle de la Venta"}
        
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
    path: '/products/new/',
    name:"product.new",
    component: ProductNewView,
    meta:{verbose_name:"Añadir Producto"},    
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
