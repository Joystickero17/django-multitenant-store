<template>
  
  <div class="dashboard">
    <b-modal ref="export_chart">
    {{ export_message }}
  </b-modal>
  <div class="row justify-content-end ml-5 mb-2">
    <div class="col-3">
      <b-button @click="exportData" variant="dark">Exportar Estadísticas</b-button>
    </div>
  </div>
    <div class="row justify-content-between mx-5 mb-4">
      
      <b-form-checkbox
      v-if="user.role == 'website_owner'"
      v-model="see_my_stats_only"
      >
      Ver solo mis estadísticas
      </b-form-checkbox>
    </div>
    <div class="row justify-content-between mx-5 mb-4">
      <div class="col-md-3">
        <b-card>
          <b-card-text>

            <h6 class="text-center">Ventas</h6>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalVentas" :duration="3"
                easing="Power1.easeOut" /></h1>
          </b-card-text>
        </b-card>
      </div>
      <div class="col-md-3">
        <b-card>
          <b-card-text>
            <h6 class="text-center">Productos</h6>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalProductos" :duration="3"
                easing="Power1.easeOut" /></h1>
          </b-card-text>
        </b-card>
      </div>
      <!-- <div class="col-md-3">
        <b-card>
          <b-card-text>

            <h6 class="text-center">Devoluciones</h6>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalDevoluciones" :duration="3"
                easing="Power1.easeOut" /></h1>
          </b-card-text>
        </b-card>
      </div> -->
      <div class="col-md-3">
        <b-card>
          <b-card-text>

            <h6 class="text-center">Usuarios</h6>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalUsuarios" :duration="3"
                easing="Power1.easeOut" /></h1>
          </b-card-text>
        </b-card>
      </div>

    </div>
    <div class="row justify-content-between mx-5">
      <div class="col-12 border rounded mx-2  p-0 d-flex">
        <div class="col-md-9 p-4">
          <div class="chart-settings d-flex justify-content-between">
            <div class="chart_title">
              <h3 class="h4">Ventas (USD)</h3>
              <span class="text-secondary">{{ chartDate }}</span>
            </div>
            <div class="chart_date_select">
              <b-button pill :pressed="chartType=='year'" @click="setYearStats()" variant="outline-secondary">Anual</b-button>
              <b-button pill :pressed="chartType=='month'" @click="setMonthStats()" class="ml-2" variant="outline-secondary">Mensual</b-button>
            </div>
          </div>
          <LineChart :labels="labels" :data_list="chart_data" ref="myChart"></LineChart>
        </div>
        <div class="col-md-3 p-0 m-0 overflow-hidden">
          <div class="border w-100">
            <p class="text-center text-secondary">Visitas</p>
            <h1 class="text-center">
              <number ref="number1" :from="0" :to="totalVisits" :duration="1" easing="Power1.easeOut" />
            </h1>
          </div>
          <div class="border w-100">
            <p class="text-center text-secondary">Reseñas</p>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalReviews" :duration="1" easing="Power1.easeOut" /></h1>
          </div>
          <div class="border w-100">
            <p class="text-center text-secondary">Freelancers</p>
            <h1 class="text-center">{{ totalFreelancers }}</h1>
          </div>
          <div class="border w-100" style="height: 80px;">

          </div>
          <div class="border w-100" style="height: 80px;">

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import LineChart from '@/components/LineChart.vue';
import { mapGetters } from 'vuex';
import axios from 'axios'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
  name: 'HomeView',
  components: {
    LineChart
  },
  data() {
    return {
      totalVentas: 0,
      cantidadVentas: 0,
      totalVisits:0,
      export_message:'',
      chart_data_loaded: false,
      labels: [],
      chart_data: [],
      totalProductos: 0,
      totalDevoluciones: 0,
      totalUsuarios: 0,
      totalFreelancers:0,
      totalReviews:0,
      chartDate: "Enero del 2023",
      chartDateYear: "",
      chartDateMonth: "",
      chartType: "year",
      
    }
  },
  computed:{
    ...mapGetters({
      options:"getStoreOptions",
      user:"getSelfUser"
    }),
    see_my_stats_only:{
      get(){
        return this.options.see_my_stats_only
      },
      set(value){
        this.setMyStatsOnlyOption(value)
      }
    }
  },
  methods:{
    setMyStatsOnlyOption(value){
      console.log(value)
      this.$store.commit("setStatsVisibilityOption", value)
      this.setGeneralStats()
    },
    exportData(){
      let current_date= new Date()
      let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      this.chartDate = current_date.toLocaleString("es-ES", options)
      this.$axios.post('/api/chart_export/', { 'year': current_date.getFullYear(),'month': current_date.getMonth()+1, 'chart_type': this.chartType, 'store_stats_only':this.see_my_stats_only }, { withCredentials: true })
      .then((res) => {
        this.export_message = res.data.message
        this.$refs["export_chart"].show()
      })
      .catch((err) => {
        console.log(err.response)
      })
    },
    setGeneralStats(){
      let current_date= new Date()
      let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      this.chartDate = current_date.toLocaleString("es-ES", options)
      this.$axios.post('/api/chart/', { 'year': current_date.getFullYear(), 'chart_type': this.chartType, 'store_stats_only':this.see_my_stats_only }, { withCredentials: true })
      .then((res) => {
        return res
      })
      .catch((err) => {
        console.log(err.response)
      })
      .then((data) => {
        let result = data.data
        this.labels = Object.keys(result.chart)
        this.totalVentas = result.total_sales_count
        this.totalProductos = result.products
        this.totalUsuarios = result.users
        this.totalReviews = result.reviews
        this.totalVisits = result.visits
        this.totalFreelancers = result.total_freelancers
        this.chart_data = Object.values(result.chart)
        this.$refs.myChart.updateChart(this.labels, this.chart_data)
      })
    },
    setYearStats(){
      this.chartType = "year"
      let current_date= new Date()
     this.$axios.post('/api/chart/', { 'year': current_date.getFullYear(), 'chart_type': this.chartType,'store_stats_only':this.see_my_stats_only }, { withCredentials: true })
      .then((res) => {
        return res
      })
      .catch((err) => {
        console.log(err.response)
      })
      .then((data) => {
        let result = data.data
        this.labels = Object.keys(result.chart)
        this.totalVentas = result.total_sales_count
        this.totalProductos = result.products
        this.totalUsuarios = result.users
        this.totalReviews = result.reviews
        this.chart_data = Object.values(result.chart)
        this.$refs.myChart.updateChart(this.labels, this.chart_data)
      })
    },
    setMonthStats(){
      this.chartType = "month"
      let current_date= new Date()
     this.$axios.post('/api/chart/', { 'year': current_date.getFullYear(), 'month': current_date.getMonth()+1, 'chart_type': this.chartType,'store_stats_only':this.see_my_stats_only }, { withCredentials: true })
      .then((res) => {
        return res
      })
      .catch((err) => {
        console.log(err.response)
      })
      .then((data) => {
        let result = data.data
        this.labels = Object.keys(result.chart)
        this.totalVentas = result.total_sales_count
        this.totalProductos = result.products
        this.totalUsuarios = result.users
        this.totalReviews = result.reviews
        this.chart_data = Object.values(result.chart)
        this.$refs.myChart.updateChart(this.labels, this.chart_data)
      })
    }
  },
  mounted() {
    this.$setupAxios()
    this.setGeneralStats()
  }
}
</script>
