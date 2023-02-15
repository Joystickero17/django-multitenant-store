<template>
    <div class="mx-5 mr-5 rounded border p-3">
        <b-modal ref="filter-modal" title="Filtros de Contactos" ok-only>
            <b-form-checkbox v-model="store_contacts_only" v-if="user.role == 'website_owner'">
                Ver solo mis contactos
            </b-form-checkbox>
        </b-modal>
        <div class="row justify-content-center">
            <div class="col-lg-6 mb-3">
                <b-input @input="getContacts()" placeholder="Buscar" v-model="search"></b-input>
            </div>
            <div class="col-4">
                <div class="filter d-flex">
                    <div @click="$refs['filter-modal'].show()" class="order-filter mx-3 d-flex align-items-center pointer">

                        <BIconFunnelFill variant="secondary"></BIconFunnelFill>
                        <span class="mx-1 p-0">Filtros</span>
                    </div>
                    <b-button @click="exportData" variant="dark">Exportar Contactos</b-button>

                </div>
            </div>
        </div>
        <b-table :fields="contact_fields" :items="contacts">
            <template #cell(profile_img)="data">
                <b-avatar :src="data.item.profile_img"></b-avatar>

            </template>
            <template #cell(first_name)="data">
                <span v-if="data.item.first_name">{{ data.item.first_name }}</span>
                <span class="bg-light p-1 d-block mt-1" v-else></span>
            </template>
            <template #cell(last_name)="data">
                <span v-if="data.item.last_name">{{ data.item.last_name }}</span>
                <span class="bg-light p-1 d-block mt-1" v-else></span>
            </template>
        </b-table>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    name: "ContactosView",
    data() {
        return {
            contacts: [],
            search: "",
            contact_fields: [
                {
                    key: "profile_img",
                    label: "Usuario"
                },
                {
                    key: "first_name",
                    label: "Nombre"
                },
                {
                    key: "last_name",
                    label: "Apellido"
                },
                {
                    key: "email",
                    label: "Correo Electrónico"
                },
                {
                    key: "total_orders",
                    label: "Compras Realizadas"
                }
            ]
        }
    },
    computed: {
        ...mapGetters({
            options: "getStoreOptions",
            user: "getSelfUser"
        }),
        store_contacts_only: {
            get() {
                return this.options.see_only_my_contacts
            },
            set(value) {
                this.$store.commit("setContactsVisibilityOption", value)
                this.getContacts()
            }
        }
    },
    methods: {
        getContacts() {
            this.$axios.get("api/contact/", { params: { search: this.search, store_contacts_only: this.store_contacts_only } })
                .then((res) => {
                    this.contacts = res.data.results

                })
                .catch()

        },
        exportData(){
            this.$axios.get("api/contact_export/", { params: { search: this.search, store_contacts_only: this.store_contacts_only } })
                .then((res) => {
                    this.contacts = res.data.results

                })
                .catch()
        }
    },
    mounted() {
        this.$setupAxios()
        this.getContacts()
    }
}
</script>