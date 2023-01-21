import App from './App.vue'
import Vue from 'vue'
import router from './router'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';
import VueApexCharts from 'vue-apexcharts'
import VueNumber from 'vue-number-animation'
import ImageUploader from 'vue-image-upload-resize'
import VueProgressBar from 'vue-progressbar'
import httpServicePlugin from './plugins/api'
//Import Froala Editor 
import 'froala-editor/js/plugins.pkgd.min.js';
//Import third party plugins
import 'froala-editor/js/third_party/embedly.min';
import 'froala-editor/js/third_party/font_awesome.min';
import 'froala-editor/js/third_party/spell_checker.min';
import 'froala-editor/js/third_party/image_tui.min';
// Import Froala Editor css files.
import 'froala-editor/css/froala_editor.pkgd.min.css';

// Import and use Vue Froala lib.
import VueFroala from 'vue-froala-wysiwyg'
Vue.use(VueFroala)
Vue.config.productionTip = false

Vue.use(httpServicePlugin)
Vue.use(VueProgressBar, {
  color: 'rgb(143, 255, 199)',
  failedColor: 'red',
  height: '2px'
})
Vue.use(ImageUploader);
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


