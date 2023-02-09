<template>
    <div class="row">
        <b-modal ref="error-modal" title="Atención">
            {{ error_message?.message }}
            
            {{ error_message?.phone_number || '' }}
            {{ error_message?.email || '' }}
            {{ error_message?.first_name || '' }}
            {{ error_message?.last_name || '' }}
        </b-modal>
        <b-modal ref="new-user" title="Crear Usuario" hide-footer>
            <label for="">Correo del Usuario:</label>
            <b-input class="mb-3"  :state="!this.errors.email.length" v-model="new_user.email"></b-input>
            <label for="">Nombre:</label>
            <b-input class="mb-3"  :state="!this.errors.first_name.length" v-model="new_user.first_name"></b-input>
            <label for="">Apellido:</label>
            <b-input class="mb-3"  :state="!this.errors.last_name.length" v-model="new_user.last_name"></b-input>
            <label for="">Teléfono</label>
            <b-input class="mb-3" :state="!this.errors.phone_number.length"  v-model="new_user.phone_number"></b-input>
            <b-button variant="success" @click="inviteUser">Invitar</b-button>
        </b-modal>
        <div v-if="user.role == 'store_owner' || user.role == 'website_owner'" class="col-12 my-3"><b-button @click="$refs['new-user'].show()" variant="success">Crear Usuario</b-button></div>
        <b-table :items="items" :fields="fields">
            <template #cell(profile_img)="data">
                <b-avatar
                :src="data.item.profile_img"
                ></b-avatar>
            </template>
            <template #cell(is_active)="data">
                <b-badge v-if="!data.item.is_active" pill variant="warning">Inactivo</b-badge>
                <b-badge v-if="data.item.is_active" pill variant="success">Activo</b-badge>
            </template>
            <template #cell(role)="data">
                {{ getRole(data.item.role) }}
            </template>

        </b-table>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            new_user:{
                email:'',
                first_name:'',
                last_name:'',
                phone_number:''
            },
            errors:{
                first_name:'',
                last_name:'',
                phone_number:'',
                email:'',
            },
            error_message:'',
            items: [],
            fields: [
                {
                    key: 'profile_img',
                    label: 'Foto'
                },
                {
                    key: 'email',
                    label: 'Email'
                },
                {
                    key: 'role',
                    label: 'Rol'
                },
                {
                    key: 'is_active',
                    label: 'Estado de la cuenta'
                }
            ]
        }
    },
    computed:{
        ...mapGetters({
            user: 'getSelfUser'
        })
    },
    methods: {
        checkForm(){
            this.errors = {}
            let any_error = false
            if (!this.new_user.email.length){
                this.errors.email = 'este campo es requerido'
                any_error=true
            }
            if (!this.new_user.phone_number.length){
                this.errors.phone_number = 'este campo es requerido'
                any_error=true
            }
            if (!this.new_user.first_name.length){
                this.errors.first_name = 'este campo es requerido'
                any_error=true
            }
            if (!this.new_user.last_name.length){
                this.errors.last_name = 'este campo es requerido'
                any_error=true
            }
            if(any_error){
                return false
            }
            return true
        },
        inviteUser(){
            if (!this.checkForm()){
                return
            }
            this.$axios.post("api/invited_user/", this.new_user)
            .then((res)=>{
                console.log(res)
            })
            .catch((err)=>{
                this.error_message = err.response.data
                this.$refs["error-modal"].show()
            })
            .finally(()=>{
                this.getItems()
                this.$refs['new-user'].hide()
                this.new_user = {
                email:'',
                first_name:'',
                last_name:'',
                phone_number:''
            }
            })
        },
        getRole(role){
            let data = {
                "website_owner":'Dueño del Sitio web',
                "store_owner":'Dueño de la Tienda',
                "store_operator":'Operador de la tienda',
                "freelance":'freelance',
                "customer":'Cliente',
                "base_user":'Usuario Base',
            }
            return data[role]
        },
        getItems() {
            this.$axios.get("api/store_users/")
                .then((res) => {
                    this.items = res.data.results
                })
                .catch((err) => {
                    console.log(err)
                })
        }
    },
    mounted() {
        this.getItems()
    }
}
</script>