<template>
    <div class="mx-5 mb-3">
        <b-modal ref='response-modal' title="Aviso">
            {{ modal_message }}
        </b-modal>
        <b-modal ref="payment-confirm-modal" title="Precaución">
            <p>¿Está seguro que desea marcar esta orden como pagada?</p>
            <p>Se ejecutaran las siguientes acciones:</p>
            <ul>
                <li>Se enviará un recibo al comprador con el cual podrá retirar la mercancia.</li>
                <li>Se acreditará dinero en la plataforma a las tiendas involucradas en la venta.</li>
                <li>En el caso de que haya asistencias por parte de algun freelancer, se acreditarán dichos puntos a su
                    cuenta.</li>
                <li class="text-danger">¡ESTA ACCIÓN NO SE PUEDE DESHACER!</li>
            </ul>
            <template #modal-footer="{cancel}">
                <b-button variant="primary" @click="cancel()">Cancelar</b-button>
                <b-button @click="updateOrderStatus" variant="danger">Confirmar Pago</b-button>
            </template>
        </b-modal>
        <div class="row mb-4" v-if="orderLoaded">
            <div class="col-lg-6 p-3 border rounded">
                <h4 class="mb-4">Resumen de la Orden</h4>
                <div class="col-6 d-inline-block">
                    <h5>Orden N°</h5>
                    <p>{{ this.$route.params.id }}</p>
                </div>
                <div class="col-6 d-inline-block">
                    <h5>Tipo de Entrega</h5>
                    <p>{{ order.delivery_type_verbose }}</p>
                </div>
                <div class="col-6 d-inline-block">
                    <h5>Fecha de Creación</h5>
                    <p>{{ order.created_at | moment('DD/MM/YYYY h:mm:ss A') }}</p>
                </div>
                <div class="col-6 d-inline-block">
                    <h5>Método de Pago:</h5>
                    {{ order.payment_type_verbose }}
                </div>
                <div class="col-6 d-inline-block">
                    <h5>Estado del pago</h5>
                    <b-badge pill variant="success" v-if="order.payment_status == 'PAYMENT_SUCCESS'">Pagado</b-badge>
                    <b-badge pill variant="warning" v-if="order.payment_status == 'AWAITING_PAYMENT'">Esperando
                        Pago</b-badge>
                    <b-button @click="$refs['payment-confirm-modal'].show()" v-if="user.role == 'website_owner' && order.payment_status != 'PAYMENT_SUCCESS'"
                        variant="light" class="rounded-circle mx-3" size="sm">
                        <BIconPencilSquare></BIconPencilSquare>
                    </b-button>
                </div>
                <div class="col-6 d-inline-block">
                    <h5>Monto Total:</h5>
                    $ {{ parseFloat(order.total_amount)?.toFixed(2) }}
                </div>

            </div>
            <div class="col-lg-6 ">
                <div class="col-12 p-3 border rounded">
                    <h4 class="mb-4">Información del cliente</h4>
                    <div class="col-6 d-inline-block">
                        <strong>Nombre</strong>
                        <p>{{ order.user_details.first_name || 'No tiene' }}</p>
                        <strong>Apellido</strong>
                        <p>{{ order.user_details.last_name || 'No tiene' }}</p>
                    </div>
                    <div class="col-6 d-inline-block">
                        <strong>Email</strong>
                        <p>{{ order.user_details.email }}</p>
                        <strong>Número de Teléfono</strong>
                        <p>{{ order.user_details.phone_number }}</p>
                    </div>
                    <div class="col-12 ">
                        <strong>Dirección de Envío</strong>
                        <p>
                            <span v-if="order.address_details?.region">
                                {{ order.address_details?.region }},
                            </span>
                            <span v-if="order.address_details?.sub_region">
                                {{ order.address_details?.sub_region }},
                            </span>
                            <span v-if="order.address_details?.city">
                                {{ order.address_details?.city }},
                            </span>
                            <br>
                            {{ order.address_details?.short_address }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="row" v-if="orderLoaded">
            <div class="col-12 p-3 border rounded">
                <div class="mt-4"
                    v-if="order.payment_method == 'pago_movil' || order.payment_method == 'transferencia_nacional'">

                    <h4>Informes de pago</h4>
                    <b-table :fields="payment_fields" :items="order.external_payments">

                    </b-table>
                </div>
                <div class="col-12">
                    <h4 class="d-inline-block">Items Ordenados</h4>
                    <a :href="this.order.receipt" class="btn btn-sm btn-dark mx-4" v-if="!!this.order.receipt">Descargar
                        Recibo</a>
                    <div class="mt-4">
                        <b-table :fields="product_fields" :items="product_orders">

                        </b-table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            order: {},
            modal_message: '',
            product_orders: [],
            product_fields: [
                {
                    key: "name",
                    label: 'Nombre del producto'
                },
                {
                    key: "store",
                    label: 'Id Tienda'
                },
                {
                    key: "price",
                    label: 'Precio'
                },
                {
                    key: "sub_total",
                    label: 'Sub Total'
                },
                {
                    key: "sub_total",
                    label: 'Sub Total'
                }
            ],
            payment_fields: [{
                key: "id",
                label: 'Id'
            }, {
                key: "payment_id",
                label: "Referencia"
            },
            {
                key: "payment_type",
                label: "Tipo"
            },
            {
                key: "national_bank",
                label: "Banco"
            },
            {
                key: "condition",
                label: "Condición"
            },

            ]
        }
    },
    methods: {
        updateOrderStatus() {
            this.$refs["payment-confirm-modal"].hide()
            let data = {
                order: this.order.id,
                is_paid: true,
            }
            this.$axios.post("api/manual_mark_paid_order/", data)
                .then((res) => {
                    this.modal_message = res.data.message
                    this.$refs["response-modal"].show()
                    this.getOrder()
                })
                .catch((err) => {
                    this.modal_message = `Ha ocurrido un error inesperado \n ${err.response.data}`
                })
        },
        getOrder() {
            this.$axios.get("/api/order/" + this.$route.params.id)
                .then((res) => {
                    this.order = res.data
                    this.getProductOrders()
                })
        },
        getProductOrders() {
            this.product_orders = this.order.product_orders.map(
                (item) => {
                    return {
                        "name": item.product_details.name,
                        "price": item.product_details.price,
                        "store": item.product_details.store,
                        "sub_total": item.product_details.price * item.quantity,
                        /* eslint-disable */
                        "condition": "NEW" ? "Nuevo" : ("USED" ? "Usado" : "Remanufacturado"),

                    }
                }
            )
        }
    },
    computed: {
        ...mapGetters({
            user: "getSelfUser",
        }),
        orderLoaded() {

            return !!Object.keys(this.order).length
        }
    },
    mounted() {
        this.$setupAxios()
        this.getOrder()
    }
}
</script>