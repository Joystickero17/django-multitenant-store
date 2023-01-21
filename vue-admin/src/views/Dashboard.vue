<template>
  <div class="dashboard">

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
      <div class="col-md-3">
        <b-card>
          <b-card-text>

            <h6 class="text-center">Devoluciones</h6>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalDevoluciones" :duration="3"
                easing="Power1.easeOut" /></h1>
          </b-card-text>
        </b-card>
      </div>
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
              <number ref="number1" :from="0" :to="totalVentas" :duration="1" easing="Power1.easeOut" />
            </h1>
          </div>
          <div class="border w-100">
            <p class="text-center text-secondary">Reseñas</p>
            <h1 class="text-center"><number ref="number1" :from="0" :to="totalReviews" :duration="1" easing="Power1.easeOut" /></h1>
          </div>
          <div class="border w-100">
            <p class="text-center text-secondary">Cantidad de Ventas</p>
            <h1 class="text-center">{{ totalVentas }}</h1>
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
      chart_data_loaded: false,
      labels: [],
      chart_data: [],
      totalProductos: 0,
      totalDevoluciones: 0,
      totalUsuarios: 0,
      totalReviews:0,
      chartDate: "Enero del 2023",
      chartDateYear: "",
      chartDateMonth: "",
      chartType: "year",
      
    }
  },
  methods:{
    setYearStats(){
      this.chartType = "year"
     this.$axios.post('/api/chart/', { 'year': 2023, 'chart_type': this.chartType }, { withCredentials: true })
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
     this.$axios.post('/api/chart/', { 'year': 2023, 'month': 1, 'chart_type': this.chartType }, { withCredentials: true })
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
   this.$axios.post('/api/chart/', { 'year': 2023, 'chart_type': this.chartType }, { withCredentials: true })
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
  // updated(){
  //   axios.post('/api/chart/',{'year':2023,'chart_type':"year"},{ withCredentials:true})
  //   .then((res)=>{
  //     return res})
  //   .catch((err)=>{
  //     console.log(err.response)
  //   })
  //   .then((data)=>{
  //     this.labels = Object.keys(data.data)
  //     this.chart_data = Object.values(data.data)
  //     this.$refs.myChart.updateChart(this.labels, this.chart_data)
  //   })

  //   }

}
</script>
