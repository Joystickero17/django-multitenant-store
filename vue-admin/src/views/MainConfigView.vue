<template>
    <div>
        <div class="mt-3 mx-5">
            <b-tabs >
                <b-tab title="Perfil" active @click="$router.push({name:'config.profile'})">
                    
                </b-tab>
                <b-tab title="Pagos" @click="$router.push({name:'config.payments'})">
                    
                </b-tab>
                <b-tab title="Usuarios" @click="$router.push('/config/users')">
                    
                </b-tab>
            </b-tabs>
        </div>
        <router-view class="mt-3 mx-5"></router-view>
    </div>
</template>