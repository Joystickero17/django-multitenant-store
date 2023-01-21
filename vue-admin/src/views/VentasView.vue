<template>
    <div class="mx-5 mr-5">
        <b-modal ref="filter-modal" hide-footer title="Seleccione el Campo a Filtrar">
            <div class="d-flex flex-column">
                <span class="text-center">Filtros</span>
                <b-form-group class="mx-5">
                    <b-form-checkbox-group id="checkbox-group-2" v-model="filters.status" name="flavour-2">
                        <b-form-checkbox value="PAYMENT_SUCCESS">Pagados</b-form-checkbox>
                        <b-form-checkbox value="AWAITING_PAYMENT">En espera de Pago</b-form-checkbox>

                    </b-form-checkbox-group>

                    <b-button class="w-100 mt-4" @click="filterOrder()">Filtrar</b-button>
                </b-form-group>
            </div>
        </b-modal>
        <div class="row my-2 justify-content-center border rounded p-3">
            <div class="offset-2 col-6">

                <b-input v-model="search" @input="searchOrder()" placeholder="Buscar Venta"></b-input>
            </div>
            <div class="col-3">
                <div class="filter d-flex">
                    <div class="order-filter d-flex align-items-center pointer">

                        <BIconFilter variant="secondary"></BIconFilter>
                        <span class="mx-1 p-0">Orden</span>
                    </div>
                    <div @click="showFilterModal()" class="order-filter mx-3 d-flex align-items-center pointer">

                        <BIconFunnelFill variant="secondary"></BIconFunnelFill>
                        <span class="mx-1 p-0">Filtros</span>
                    </div>

                </div>
            </div>
        </div>
        <div class="row justify-content-center border rounded px-3">
            <div class="col-12">

                <b-table hover 
                :busy="isBusy" 
                :items="items" 
                :empty-filtered-text="'resultados'"
                :empty-text="'No hay registros para mostrar'"
                :fields="fields" 
                show-empty>
                    <template #cell(payment_status)="data">
                        <b-badge pill variant="success"
                            v-if="data.item.payment_status == 'PAYMENT_SUCCESS'">Pagado</b-badge>
                        <b-badge pill variant="warning" v-if="data.item.payment_status == 'AWAITING_PAYMENT'">Esperando
                            Pago</b-badge>
                    </template>

                    <template #empty="scope">
                        <div class="d-flex flex-column align-items-center">

                            <img src="/static/img/no_results.svg"  class="w-25" alt="">                        
                            <h5 class="text-center">{{ scope.emptyText }}</h5>
                        </div>
                        
                    </template>
                    <template #emptyfiltered="scope">
                        <h4 class="text-center">{{ scope.emptyFilteredText }}</h4>
                    </template>
                    <template #cell(total_order)="data">
                        {{ '$' + data.item.total_order }}
                    </template>
                    <template #table-busy>
                        <div class="text-center text-danger my-2">
                            <b-spinner class="align-middle"></b-spinner>
                            <strong>Cargando...</strong>
                        </div>
                    </template>
                    <template #cell(action)="data">
                        <b-button @click="goDetail(data.item.id)" variant="light">
                            <BIconPencilSquare></BIconPencilSquare>
                        </b-button>
                        <b-button class="mx-2" variant="light">
                            <BIconTrashFill></BIconTrashFill>
                        </b-button>

                    </template>
                </b-table>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="mt-3">
                <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="5"
                    @input="searchOrder($event)"></b-pagination>
            </div>
        </div>
    </div>
</template>
<script>
import { BIconPencilSquare, BIconTrashFill } from 'bootstrap-vue'
export default {
    methods: {
        goDetail(id) {
            this.$router.push({ name: "ventas.detail", params: { id: id } })
        },
        showFilterModal() {
            this.$refs['filter-modal'].show()
        },
        filterOrder() {
            this.isBusy = true
            this.$axios.get("/api/order/", { params: { search: this.search, page: 1, status: this.filters.status } })
                .then((res) => {
                    this.items = res.data.results
                    this.totalRows = res.data.count
                    this.currentPage = res.data.current_page
                    this.isBusy = false
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        searchOrder(page = 1) {
            this.isBusy = true
            this.$axios.get("/api/order/", { params: { search: this.search, page: page, status: this.filters.status } })
                .then((res) => {
                    this.items = res.data.results
                    this.totalRows = res.data.count
                    this.currentPage = res.data.current_page
                    this.isBusy = false
                })
                .catch((err) => {
                    console.log(err)
                })
        }
    },
    components: {
        BIconPencilSquare,
        BIconTrashFill
    },
    data() {
        return {
            filters: {
                status: [
                    "PAYMENT_SUCCESS",
                    "AWAITING_PAYMENT"
                ]
            },
            currentPage: 1,
            totalRows: 0,
            isBusy: true,
            search: '',
            fields: [
                {
                    key: 'id',
                    label: "Nro",
                    sortable: true
                },
                {
                    key: 'payment_type_verbose',
                    label: "Método de Pago",
                    sortable: false
                },
                {
                    key: 'payment_status',
                    label: 'Estado del Pago',
                    sortable: true,
                },
                {
                    key: 'delivery_type_verbose',
                    label: 'Tipo de Entrega',
                    sortable: true,
                },
                {
                    key: 'total_order',
                    label: 'Total de la Orden',
                    sortable: true,
                },
                {
                    key: 'action',
                    label: 'Acción',

                },
            ],
            xd: ["N°", "Metodo de Pago", "Estado del Pago", "Tipo de Entrega", "Total Orden ($)", "Fecha", "Acción"],
            items: [],
        }
    },
    mounted() {
        this.isBusy = true
        this.$axios.get("/api/order/")
            .then((res) => {
                this.items = res.data.results
                this.totalRows = res.data.count
                this.currentPage = res.data.current_page
                this.isBusy = false
            })
            .catch((err) => {
                console.log(err)
            })
    }

}
</script>