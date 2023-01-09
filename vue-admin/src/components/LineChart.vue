<template>
    <div style="max-width: 55vw;">

        <apexChart ref="lineChart" height="300" type="line" :options="chartOptions" :series="series"></apexChart>
    </div>
</template>
<script>


export default {
    components: {},
    props: [
        "labels",
        "data_list"
    ],
    computed: {
        chartData() {
            return this.initial_data
        }
    },
    methods: {
        updateChart(labels, data) {
            console.log("XD")
            this.chartOptions = {
                ...this.chartOptions, ...{
                    xaxis: {
                        categories: labels,
                    }
                }
            }
            // this.$refs.lineChart.updateSeries(
            //     [
            //     {
            //         name: 'ventas_mes',
            //         data: this.data_list
            //     }
            // ]
            // )
            this.series = [
                {
                    name: 'ventas_mes',
                    data: data
                }
            ]
        },
        refreshChart() {
            console.log("XD")
            this.chartOptions = {
                ...this.chartOptions, ...{
                    xaxis: {
                        categories: this.labels,
                    }
                }
            }
            // this.$refs.lineChart.updateSeries(
            //     [
            //     {
            //         name: 'ventas_mes',
            //         data: this.data_list
            //     }
            // ]
            // )
            this.series = [
                {
                    name: 'ventas_mes',
                    data: this.data_list
                }
            ]
        }
    },  
    data() {
        return {
            chartOptions: {
                chart: {
                    id: 'vuechart-example'
                },
                xaxis: {
                    categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
                },
                stroke:{
                    curve:'smooth'
                }
                
            },
            series: [{
                name: 'series-1',
                data: [0, 0, 0, 0, 0, 0, 0, 0]
            }]
        }
    },
    mounted(){
        this.refreshChart()
    }
}
</script>
<style>

</style>