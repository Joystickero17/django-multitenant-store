<template>
    <div class="mx-5 mb-3">
        {{  }}
        <div class="row" v-if="orderLoaded">
            <div class="col-lg-6">

                <h5>Orden N°</h5>
                <p>{{ this.$route.params.id }}</p>
                <h5>Tipo de Entrega</h5>
                <p>{{ order.delivery_type_verbose }}</p>
                <h5>Fecha de Creación</h5>
                <p>{{ order.created_at | moment('DD/MM/YYYY h:mm:ss A') }}</p>
                <h5>Metodo de Pago:</h5>
                {{order.payment_type_verbose}}
                <div class="mt-4" v-if="order.payment_method == 'pago_movil' || order.payment_method == 'transferencia_nacional'">
                    <b-table :fields="payment_fields" :items="order.external_payments">

                    </b-table>
                </div>
            </div>
            <div class="col-lg-6">
                <h3>
                    <b-badge pill variant="success" v-if="order.payment_status == 'PAYMENT_SUCCESS'">Pagado</b-badge>
                    <b-badge pill variant="warning" v-if="order.payment_status == 'AWAITING_PAYMENT'">Esperando
                        Pago</b-badge>
                </h3>
            </div>

        </div>

    </div>
</template>
<script>
export default {
    data() {
        return {
            order: {},
            payment_fields:[{
                key:"id",
                label:'Id'
            },{
                key:"payment_id",
                label:"Referencia"
            },
            {
                key:"payment_type",
                label:"Tipo"
            },
            {
                key:"national_bank",
                label:"Banco"
            },
            {
                key:"state",
                label:"Estado"
            },

        ]
        }
    },
    methods: {
        getOrder() {
            this.$axios.get("/api/order/" + this.$route.params.id)
                .then((res) => {
                    this.order = res.data
                })
        }
    },
    computed:{
        orderLoaded(){

            return !!Object.keys(this.order).length
        }
    },
    mounted() {
        this.getOrder()
    }
}
</script>