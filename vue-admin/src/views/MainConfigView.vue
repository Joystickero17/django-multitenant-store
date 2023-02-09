<template>
    <div>
        <div class="mt-3 mx-5">
            <b-tabs >
                <b-tab title="Perfil" active @click="$router.push({name:'config.profile'})">
                    
                </b-tab>
                <div v-if="user.store_details">
                    <b-tab title="Pagos" v-if="user.role=='store_owner' || user.roler=='website_owner'" @click="$router.push({name:'config.payments'})">
                    
                    </b-tab>

                    <b-tab title="Usuarios" @click="$router.push('/config/users')">
                    
                    </b-tab>
                </div>
            </b-tabs>
        </div>
        <router-view class="mt-3 mx-5"></router-view>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data(){
        return {

        }
    },
    computed:{
        ...mapGetters(
            {
                user:'getSelfUser'
            }
        )
    }
}
</script>