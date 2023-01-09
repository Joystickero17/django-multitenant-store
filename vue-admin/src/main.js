import App from './App.vue'
import Vue from 'vue'
import router from './router'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';
import VueApexCharts from 'vue-apexcharts'
import VueNumber from 'vue-number-animation'
Vue.use(require('vue-moment'));
Vue.use(VueNumber)
Vue.use(VueApexCharts)
Vue.component('apexChart', VueApexCharts)
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')


