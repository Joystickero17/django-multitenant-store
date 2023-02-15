<template>
    <div class="mx-5">
        <div class="row my-4">
            <div class="col-3">
                <b-button variant="success" @click="$router.push({name:'config.storages.new'})">Agregar un Almacén</b-button>
            </div>
            <div class="col-6 offset-1">
                <b-input @input="getItems" v-model="search" placeholder="Buscar Almacén"></b-input>
            </div>            
        </div>
        <b-table
        :items="items"
        :fields="fields"
        >    
        <template #cell(storage_type)="data">
            {{ data.item.storage_type == "tienda_fisica" ? "Tienda Física": "Almacén" }}

        </template>
        <template #cell(store)="data">
            {{ data.item.store_details.name }}

        </template>
        <template #cell(city)="data">
            {{ data.item.city || 'No especificada' }}

        </template>
        <template #cell(action)="data">
            <b-button variant="light" @click="$router.push({name:'config.storages.detail', params:{id:data.item.id}})"><BIconPencilSquare></BIconPencilSquare></b-button>

        </template>
        </b-table>
    </div>
</template>
<script>
export default {
    data(){
        return {
            search:'',
            items:[],
            fields:[
                {
                    key:'storage_type',
                    label: 'Tipo de Almacén'
                },
                {
                    key:'store',
                    label:'tienda'
                },
                {
                    key:'region',
                    label:'Estado'
                },
                {
                    key:'subregion',
                    label:'Municipio'
                },
                {
                    key:'city',
                    label:'Ciudad'
                },
                {
                    key:'action',
                    label:'Acción'
                },
            ]

        }
    },
    methods:{
        getItems(){
            this.$axios.get("api/product_storage/", {params:{search:this.search}})
            .then((res)=>{
                this.items = res.data.results
            })
            .catch((err)=>{
                console.log(err)
            })
        }
    },
    mounted(){
        this.getItems()
    }
}
</script>