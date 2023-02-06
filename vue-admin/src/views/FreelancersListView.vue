<template>
    <div>
        <div class="row mx-5 mb-4 ">
            <b-modal ref="filter-modal" hide-footer title="Filtros">
                <b-form-group label="Estados">
                <b-form-checkbox-group
                v-model="states"
                >
                <b-form-checkbox :value="true">Completados</b-form-checkbox>
                <b-form-checkbox :value="false">No Completados</b-form-checkbox>
                </b-form-checkbox-group>
                
                </b-form-group>
                <b-form-group label="Calificaciones">
                <b-form-checkbox-group
                v-model="feedback"
                >
                <b-form-checkbox :value="true">Positiva</b-form-checkbox>
                <b-form-checkbox :value="false">Negativa</b-form-checkbox>
                </b-form-checkbox-group>
                
                </b-form-group>
                <b-button @click="getItems()">Filtrar</b-button>
            </b-modal>
            <div class="col-lg-4">
                <b-card class="h-100">
                    <b-card-text class="d-flex flex-column align-items-center">
                        <h6>Freelance Destacado</h6>
                        <b-avatar :src="best_freelancer.profile_img" size="6rem"></b-avatar>
                        
                    </b-card-text>
                </b-card>
            </div>
            <div class="col-lg-4">
                <b-card class="h-100">
                    <b-card-text class="d-flex flex-column align-items-center justify-content-center">
                        <h6>Ordenes Asistidas</h6>
                        <h1 class="display-3"><number ref="assistance_number" :from="0" :to="received_assistances"></number></h1>

                    </b-card-text>
                </b-card>
            </div>
            <div class="col-lg-4">
                <b-card class="h-100">
                    <b-card-text class="d-flex flex-column align-items-center">
                        <h6>Cliente Mejor Asistido</h6>
                        <b-avatar :src="most_assisted_customer.profile_img" size="6rem"></b-avatar>
                    </b-card-text>
                </b-card>
            </div>
        </div>
        <div class="row mx-5 mb-4 p-3 border rounded">
            <div class="col-6 offset-3">
                <b-input v-model="search" placeholder="Buscar" @input="getItems()"></b-input>
            </div>
            <div class="col-3 d-flex flex-column justify-content-center">
                <div class="filters">

                    <div @click="$refs['filter-modal'].show()" class="order-filter mx-3 d-flex align-items-center pointer">
        
                    <BIconFunnelFill variant="secondary"></BIconFunnelFill>
                    <span class="mx-1 p-0">Filtros</span>
                </div>
                </div>
            </div>
        </div>
        <div class="row mx-5 mb-4 p-4 border rounded">
    
            <b-table
            striped hover
            :items="items"
            :fields="fields"
            >
            <template #cell(feedback)="data">
                <span :class="{
                    'text-success font-weight-bold':!!data.item.feedback,
                    'text-danger font-weight-bold':!data.item.feedback,
                    'text-dark font-weight-bold':data.item.feedback==null
                    }">
                    
                {{ data.item.feedback == null ? 'Sin Calificar': data.item.feedback ? 'Positiva':'Negativa' }}
                </span>
            
            </template>
            <template #cell(completed)="data">
                <span :class="{'text-success font-weight-bold':!!data.item.completed,'text-danger font-weight-bold':!data.item.completed}">
                    
                {{ data.item.completed == null ? 'En proceso': data.item.completed ? 'Completada' : 'No completada'}}
                </span>
            
            </template>
            <template #cell(customer_details)="data">
                <b-avatar :src="data.item.customer_details.profile_img"></b-avatar>
                <span class="mx-3">{{ data.item.customer_details.email }}</span>
            </template>
            <template #cell(freelance_details)="data">
                <b-avatar :src="data.item.freelance_details.profile_img"></b-avatar>
                <span class="mx-3">{{ data.item.freelance_details.email }}</span>
            </template>
            <template #cell(product_orders)="data">
                {{ data.item.product_orders.length+data.item.cart_items.length }}
            </template>
        </b-table>    
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data(){
        return {
            search:'',
            states:[],
            feedback:[],
            items:[],
            fields:[
                {
                    key:'freelance_details',
                    label:'Freelance Asistente'
                },
                {
                    key:'customer_details',
                    label:'Cliente Asistido'
                },
                {
                    key:"feedback",
                    label:"Calificación",
                    sortable:true
                },
                {
                    key:"completed",
                    label:'Estado',
                    sortable:true
                },
                {
                    key:'product_orders',
                    label:'Cantidad de Productos',
                    sortable:true
                }
            ],
            best_freelancer:{},
            most_assisted_customer:{},
            received_assistances:0
        }
    },
    computed:{
        ...mapGetters({
            user:"getSelfUser"
        })
    },
    methods:{
        getStats(){
            this.$axios.get("api/freelancers_stats/")
            .then((res)=>{
                
                this.best_freelancer = res.data.best_freelance
                this.most_assisted_customer = res.data.most_assisted_customer
                this.received_assistances = res.data.assist_received
            })
            .catch((err)=>{
                console.log(err.response)
            })
        },

        getItems(){
            this.$axios("api/assistance/", {params:{search:this.search,states:this.states,feedback:this.feedback}})
            .then((res)=>{
                this.items = res.data.results
            })
            .catch((err)=>{
                console.log(err.response.data)
            })
        }
    },
    mounted(){
        this.$setupAxios()
        this.getStats()
        this.getItems()
    }
}
</script>