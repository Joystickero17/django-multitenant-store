<template>
    <div class="mx-5">
        <router-view></router-view>
        <b-modal ref="payment-method" title="Registrar Métodos de Pago" hide-footer>
            <label>Tipo:</label>
            <b-form-select class="mb-3" :options="type_options" v-model="payment_method.type"></b-form-select>
            
            <label>Numero de Cuenta (Si aplica)</label>
            <b-input class="mb-3" v-model="payment_method.account_number"></b-input>
            <label>Email asociado (Si aplica)</label>
            <b-input class="mb-3" v-model="payment_method.email_adress"></b-input>
            <label>Numero de Teléfono</label>
            <b-input class="mb-3" v-model="payment_method.phone_number"></b-input>
            <label>Banco (Si aplica)</label>
            <b-form-select class="mb-3" v-model="payment_method.national_bank" :options="bank_options"></b-form-select>

            <b-button @click="addPaymentMethodToList">Agregar</b-button>
        </b-modal>
        <b-modal ref="response-modal" title="Atención">
            {{ response }}
        </b-modal>

        <b-modal ref="photo-img" title="Cambiar foto de perfil" hide-footer>
            <b-form-file @input="loadB64" placeholder="Seleccione un Archivo">

            </b-form-file>

            <b-button class="mt-3" @click="updateProfileImg"
                v-if="user?.profile_img != null && user?.profile_img != ''">Guardar</b-button>
        </b-modal>
        <div class="row border p-3">
            <div class="col-12 mb-2">
                <h4>Datos del Usuario</h4>
            </div>
            <div class="col-3">
                <b-avatar @click.native="$refs['photo-img'].show()" :src="user?.profile_img" class="cursor-pointer"
                    size="12rem"></b-avatar>
            </div>
            <div class="col-9">
                <div class="col-5 d-inline-block">

                    <label for="">Nombre</label>
                    <b-input v-model="user.first_name"></b-input>
                    <label for="">Apellido</label>
                    <b-input v-model="user.last_name"></b-input>
                    <label for="">Teléfono de contacto</label>
                    <b-input v-model="user.phone_number"></b-input>
                </div>
                <div class="col-5  mx-2 d-inline-block">
                    <label for="">Rol Actual</label>
                    <b-input v-model="userRole" readonly></b-input>
                    <label for="">Acerca de mi</label>
                    <b-form-textarea v-model="user.about" rows="3" no-resize></b-form-textarea>
                </div>
                <div class="col-12 my-3">
                    <b-button @click="updateProfileUser">Guardar Cambios</b-button>
                </div>
            </div>
        </div>
        <div v-if="user.role == 'store_owner'" class="row border p-3 my-4">

            <div class="col-4">
                <h3>Metodos de Retiro</h3>
            </div>
            <div class="col-6">
                <b-button @click="$refs['payment-method'].show()" variant="success">Agregar Metodo de Retiro</b-button>
            </div>

            <div class="col-12">
                <b-table :fields="pm_fields" :items="user.payment_methods">
                    <template #cell(national_bank)="data">
                        {{ getBank(data.item.national_bank) }}
                    </template>
                    <template #cell(action)="data">
                        <b-button @click="removePaymentMethod(data.item.id)" variant="light">
                            <BIconTrashFill></BIconTrashFill>
                        </b-button>
                    </template>
                </b-table>
            </div>
        </div>
    </div>
</template>
<style scoped>
.cursor-pointer {
    cursor: pointer;
}
</style>
<script>
import { mapGetters } from 'vuex'
export default {
    computed: {
        ...mapGetters({
            state_user: "getSelfUser"
        }),
        userRole() {

            return this.getRole(this.user.role)
        }
    },
    methods: {
        loadB64(e) {
            const reader = new FileReader()
            reader.addEventListener('load', () => {
                this.b64_profile_img = reader.result
            })
            reader.readAsDataURL(e)
        },
        updateProfileImg() {
            if (this.b64_profile_img == null || this.b64_profile_img == '') {
                console.log(this.b64_profile_img)
                return
            }
            this.$axios.patch(`api/same_user/${this.state_user.id}/`, { profile_img: this.b64_profile_img })
                .then((res) => {
                    console.log(res)
                    this.response = 'Foto de perfil actualizada con éxito'
                    this.$refs['response-modal'].show()
                    this.user.profile_img = res.data.profile_img
                })
                .catch((err) => {
                    console.log(err)
                    this.response = 'Ha ocurrido un error al actualizar tu foto de perfil'
                    this.$refs['response-modal'].show()
                })
                .finally(() => {
                    this.$store.dispatch("retieveUser")
                })
        },
        addPaymentMethodToList(){
            this.user.payment_methods.push(this.payment_method)
            this.payment_method = {
                type: '',
                account_number: '',
                email_adress: '',
                phone_number: '',
                national_bank: '',
            }
            
        },
        removePaymentMethod(id){
            this.user.payment_methods = this.user.payment_methods.filter(item=>item.id!=id)
        },
        updatePaymentMethod(){

            if (!this.new_paymen_methods.length){
                return
            }
            this.$axios.patch(`api/same_user/${this.user.id}/`, {payment_methods:this.new_payment_methods})
            .then((res)=>{
                console.log(res)
                this.$refs['payment_method'].hide()
            })
            .finally(() => {
                    this.$store.dispatch("retieveUser")
                })
        },
        getBank(code){
            return this.bank_options.find((item)=>{return item.value==code})?.text
        },
        updateProfileUser() {
            let data = {
                first_name: this.user.first_name,
                last_name: this.user.last_name,
                about: this.user.about,
                phone_number: this.user.phone_number,
                payment_methods: this.user.payment_methods
            }
            this.$axios.patch(`api/same_user/${this.user.id}/`, data)
                .then((res) => {
                    console.log(res)
                    this.response = 'Perfil actualizado con éxito'
                    this.$refs['response-modal'].show()
                    this.$store.dispatch("retieveUser")
                })
                .catch((err) => {
                    console.log(err)
                    this.response = 'Ha ocurrido un error al actualizar tu Perfil'
                    this.$refs['response-modal'].show()
                })
        },
        getRole(role) {
            let data = [
                {
                    "value": "website_owner",
                    "display_name": "Dueño del sitio Web"
                },
                {
                    "value": "base_user",
                    "display_name": "Usuario sin rol"
                },
                {
                    "value": "store_owner",
                    "display_name": "Dueño de Tienda"
                },
                {
                    "value": "store_operator",
                    "display_name": "Operador de tienda"
                },
                {
                    "value": "freelance",
                    "display_name": "Freelance"
                },
                {
                    "value": "customer",
                    "display_name": "Cliente"
                },
                {
                    "value": "random_role",
                    "display_name": "Rol de Prueba"
                }
            ]
            return data.find((item) => {
                return item.value == role
            })?.display_name
        }
    },
    data() {
        return {
            user: {},
            response: '',
            pm_fields:[
                {
                    key:"type",
                    label: 'Tipo de Pago'
                },
                {
                    key:"account_number",
                    label: 'Numero de Cuenta'
                },
                {
                    key:"email_adress",
                    label: 'Correo Asociado'
                },
                {
                    key:"phone_number",
                    label: 'Teléfono'
                },
                {
                    key:"national_bank",
                    label: 'Banco'
                },
                {
                    key:"action",
                    label: 'Acción'
                },
            ],
            type_options:[
                {text:"PAYPAL" ,value:"paypal"},
                {text:"PAGO MOVIL" ,value:"pago_movil"},
                {text:"TRANSFERENCIA" ,value:"transferencia_nacional"}
            ],
            bank_options: [
                { text: "BANCO DE VENEZUELA", value: "0102" },
                { text: "BANCO VENEZOLANO DE CREDITO", value: "0104" },
                { text: "BANCO MERCANTIL", value: "0105" },
                { text: "BANCO PROVINCIAL", value: "0108" },
                { text: "BANCARIBE", value: "0114" },
                { text: "BANCO EXTERIOR", value: "0115" },
                { text: "BANCO CARONI", value: "0128" },
                { text: "BANESCO BANCO UNIVERSAL", value: "0134" },
                { text: "SOFITASA", value: "0137" },
                { text: "BANCO PLAZA", value: "0138" },
                { text: "BANGENTE", value: "0146" },
                { text: "BANCO FONDO COMUN", value: "0151" },
                { text: "CIEN POR CIENTO BANCO", value: "0156" },
                { text: "DEL SUR BANCO UNIVERSAL", value: "0157" },
                { text: "BANCO DEL TESORO", value: "0163" },
                { text: "BANCO AGRICOLA DE VENEZUELA", value: "0166" },
                { text: "BANCRECER", value: "0168" },
                { text: "BANCO MICROFINANCIERO", value: "0169" },
                { text: "BANCO ACTIVO", value: "0171" },
                { text: "BANCAMIGA", value: "0172" },
                { text: "BANPLUS", value: "0174" },
                { text: "BANCO BICENTENARIO DEL PUEBLO", value: "0175" },
                { text: "BANFANB", value: "0177" },
                { text: "BANCO NACIONAL DE CREDITO", value: "0191" },
            ],
            payment_method: {
                type: '',
                account_number: '',
                email_adress: '',
                phone_number: '',
                national_bank: '',
            },
            new_payment_methods:[],
            b64_profile_img: '',
        }

    },
    mounted() {
        this.$setupAxios()
        this.$axios.get(`api/same_user/`)
            .then((res) => {
                this.user = res.data.results[0]
                this.new_payment_methods = this.user.payment_methods
            })
            .catch((err) => {
                console.log(err)
            })
    }
}
</script>