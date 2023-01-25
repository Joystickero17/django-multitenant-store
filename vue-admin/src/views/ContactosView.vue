<template>
    <div class="mx-5 mr-5 rounded border p-3">
        <div class="row justify-content-center">
            <div class="col-lg-6 mb-3">

                <b-input @input="getContacts()" placeholder="Buscar" v-model="search"></b-input>
            </div>
        </div>
        <b-table
        :fields="contact_fields"
        :items="contacts"
        ></b-table>
    </div>
</template>
<script>
export default {
    name:"ContactosView",
    data(){
        return{
            contacts:[],
            search:"",
            contact_fields:[
                {
                    key:"first_name",
                    label:"Nombre"
                },
                {
                    key:"last_name",
                    label:"Apellido"
                },
                {
                    key:"email",
                    label:"Correo Electrónico"
                },
                {
                    key:"total_orders",
                    label:"Compras Realizadas"
                }
            ]
        }
    },
    methods:{
        getContacts(){
            this.$axios.get("api/contact/", {params:{search:this.search}})
            .then((res)=>{
                this.contacts = res.data.results

            })
            .catch()

        }
    },
    mounted(){
        this.$setupAxios()
        this.getContacts()
    }
}
</script>