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
import ChatView from '@/views/ChatView.vue'
import FreelanceResumeView from '@/views/FreelanceResumeView.vue'
import FreelancersListViewVue from '@/views/FreelancersListView.vue'
import ConfigView from '@/views/ConfigView.vue'
import UserPaymentsView from '@/views/UserPaymentsView.vue'
import UsersListView from '@/views/UsersListView.vue'
import MainConfigView from '@/views/MainConfigView.vue'
import StorageList from "@/views/StorageList.vue"
import StorageDetail from "@/views/StorageDetail.vue"
import StorageNew from "@/views/StorageNew.vue"
import ExportFilesView from "@/views/ExportFilesView.vue"

Vue.use(VueRouter)

const routes = [
  {
    path:"/config",
    name:"config",
    redirect: '/config/profile/',
    component:MainConfigView,
    meta:{verbose_name:"Configuración"},
    children:[
      {
        path:"profile",
        component:ConfigView,
        name:'config.profile'
      },
      {
        path:"payments",
        component:UserPaymentsView,
        name:'config.payments'
      },
      {
        path:"users",
        component:UsersListView,
        name:'config.users'
      },
      {
        path:"storages",
        component:StorageList,
        name:'config.storages'
      },
      {
        path:"storages/edit/:id",
        component:StorageDetail,
        name:'config.storages.detail'
      },
      {
        path:"storages/new/",
        component:StorageNew,
        name:'config.storages.new'
      }
    ]
  },
  {
    path: '/freelancers-list',
    name: 'freelancers.list',
    component: FreelancersListViewVue,
    meta:{verbose_name:"Asistencias Freelancers"}
  },
  {
    path: '/freelance-resume',
    name: 'freelance.resume',
    component: FreelanceResumeView,
    meta:{verbose_name:"Estadisticas"}
  },
  {
    path: '/',
    name: 'dashboard',
    component: DashboardVue,
    meta:{verbose_name:"Estadisticas"}
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatView,
    meta:{verbose_name:"MLS Chat"}
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
  {
    path: '/exports',
    name:"export_files",
    component: ExportFilesView,
    meta:{verbose_name:"Mis Archivos Exportados"},    
  },

]

const router = new VueRouter({
  routes,
  mode: "history",
  base:"/store-admin/"
})
export default router
