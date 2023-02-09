<template>
    <div class="mx-5">
        <router-view></router-view>
        <b-modal ref="response-modal" title="Atención">
            {{ response }}
        </b-modal>
        
        <b-modal ref="photo-img" title="Cambiar foto de perfil" hide-footer>
            <b-form-file @input="loadB64" placeholder="Seleccione un Archivo">

            </b-form-file>
            
            <b-button class="mt-3" @click="updateProfileImg" v-if="user?.profile_img != null && user?.profile_img != ''">Guardar</b-button>
        </b-modal>
        <div class="row border p-3">
            <div class="col-12 mb-2">
                <h4>Datos del Usuario</h4>
            </div>
            <div class="col-3" >
                <b-avatar @click.native="$refs['photo-img'].show()"
                :src="user?.profile_img"
                class="cursor-pointer"
                size="12rem"
                ></b-avatar>
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
                    <b-form-textarea
                    v-model="user.about"
                    rows="3"
                    no-resize
                    ></b-form-textarea>
                </div>
                <div class="col-12 my-3">
                    <b-button @click="updateProfileUser">Guardar Cambios</b-button>
                </div>
            </div>
        </div>

    </div>
</template>
<style scoped>
.cursor-pointer{
    cursor:pointer;
}
</style>
<script>
import { mapGetters } from 'vuex'
export default {
    computed:{
        ...mapGetters({
            state_user:"getSelfUser"
        }),
        userRole(){

                return this.getRole(this.user.role)
            }
    },
    methods:{
        loadB64(e){
            const reader = new FileReader()
            reader.addEventListener('load', ()=>{
                this.b64_profile_img = reader.result
            })
            reader.readAsDataURL(e)
        },
        updateProfileImg(){
            if (this.b64_profile_img == null || this.b64_profile_img == ''){
                console.log(this.b64_profile_img)
                return
            }
            this.$axios.patch(`api/same_user/${this.state_user.id}/`, {profile_img:this.b64_profile_img})
            .then((res)=>{
                console.log(res)
                this.response='Foto de perfil actualizada con éxito'
                this.$refs['response-modal'].show()
                this.user.profile_img = res.data.profile_img
            })
            .catch((err)=>{
                console.log(err)
                this.response='Ha ocurrido un error al actualizar tu foto de perfil'
                this.$refs['response-modal'].show()
            })
            .finally(()=>{
                this.$store.dispatch("retieveUser")
            })
        },
        updateProfileUser(){
            let data = {
                first_name: this.user.first_name,
                last_name: this.user.last_name,
                about: this.user.about,
                phone_number:this.user.phone_number,

            }
            this.$axios.patch(`api/same_user/${this.user.id}/`, data)
            .then((res)=>{
                console.log(res)
                this.response='Perfil actualizado con éxito'
                this.$refs['response-modal'].show()
                this.$store.dispatch("retieveUser")
            })
            .catch((err)=>{
                console.log(err)
                this.response='Ha ocurrido un error al actualizar tu Perfil'
                this.$refs['response-modal'].show()
            })
        },
        getRole(role){
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
            return data.find((item)=>{
                return item.value == role
            })?.display_name
        }
    },
    data(){
        return {
            user:{},
            response:'',
            b64_profile_img:'',
        }

    },
    mounted(){
        this.$setupAxios()
        this.$axios.get(`api/same_user/`)
        .then((res)=>{
            this.user = res.data.results[0]
        })
        .catch((err)=>{
            console.log(err)
        })
        }
}
</script>