<template>
    <div>
        <b-modal ref='error-modal'>
            <div v-for="err in error" :key="err">
                {{ err }}
            </div>
        </b-modal>
        <b-modal title="Solicitar pago" ref="payment-modal">
            <p>Seleccione el monto a retirar</p>

            <b-input type="number" min="0" :max="getUserMoney" v-model="money"></b-input>
            <template #modal-footer="{ cancel }">
                <b-button size="sm" variant="danger" @click="cancel()">
                    Cancelar
                </b-button>
                <!-- Button with custom close trigger value -->
                <b-button size="sm" variant="outline-secondary" @click="requestPayment">
                    Enviar
                </b-button>
            </template>
        </b-modal>
        <div class="row border rounded p-3">
            <div class="col-6">
                <b-input placeholder="Buscar Pago"></b-input>
            </div>
            <div class="col-6">
                <b-button @click="$refs['payment-modal'].show()">Solicitar Pago</b-button>
            </div>
        </div>
        <div class="row">

            <b-table :items="items" :fields="fields">
                <template #cell(paid)="data">
                    <b-badge v-if="!data.item.paid" pill variant="warning">En proceso</b-badge>
                    <b-badge v-if="data.item.paid" pill variant="success">Pagada</b-badge>
                </template>
                <template #cell(created_at)="data">
                    <span>{{ data.item.created_at | moment('DD/MM/YYYY, h:mm:ss a') }}</span>
                </template>
                <template #cell(payment_date)="data">
                    
                    <span>{{ data.item.payment_date | moment('DD/MM/YYYY, h:mm:ss a') }}</span>
                </template>
            </b-table>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            money: 0,
            error: [],
            fields: [
                {
                    key: 'id',
                    label: "Id del Pago"
                },
                {
                    key: 'user',
                    label: "Usuario Solicitante"
                },
                {
                    key: 'money',
                    label: "Monto a Retirar",
                    sortable: true
                },
                {
                    key: 'paid',
                    label: 'Pagado',
                    sortable: true
                },
                {
                    key: 'created_at',
                    label: 'Fecha de solicitud',
                    sortable: true
                },
                {
                    key: 'payment_date',
                    label: 'Fecha de pago',
                    sortable: true
                }
            ],
            items: []
        }
    },
    computed: {
        ...mapGetters({
            user: "getSelfUser"
        }),
        getUserMoney() {
            return this.user.store_details?.money || this.user.credits || 0
        }
    },
    methods: {
        getItems() {
            this.$axios.get("api/user_payments/")
                .then((res) => {
                    this.items = res.data.results
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        requestPayment() {
            this.$axios.post('api/user_payments/', { money: this.money })
                .then((res) => {
                    console.log(res)
                    this.$refs['payment-modal'].hide()
                    this.getItems()
                    this.$store.dispatch("retieveUser")
                })
                .catch((err) => {
                    this.error = err.response.data?.message
                    this.$refs["error-modal"].show()
                })
            
        }
    },
    mounted() {
        this.$setupAxios()
        this.getItems()
    }

}
</script>