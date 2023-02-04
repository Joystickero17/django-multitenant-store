<template>
    <div class="row m-0 p-3" style="height: 80px;">
        
        <b-modal title="Notificaciones" ref="notification-modal">
            <h4 v-if="!notifications.length">Hurra! no hay notificaciones aún</h4>
            <div v-for="not, index in notifications" :key="index" class="border notification rounded">
                <p class="notification__type">Tipo: {{ not.entity_name }}</p>
                <p class="notification__description">{{ not.message }}</p>
                <p class="notification__created_at"> {{ not.created_at| moment('DD/MM/YYYY h:mm:ss A') }}</p>

            </div>
        </b-modal>
        <div class="col-md-6 d-flex align-items-center">
            <h5>{{ this.$route.meta.verbose_name }}</h5>
        </div>
        <div class="col-md-6 d-flex justify-content-center align-items-center" style="height: 40px;">
            <div class="notifications p-4">
                <a :href="getStoreUrl">
                    <BIconShop font-scale="1.5" variant="secondary"></BIconShop>
                </a>
            </div>
            <div class="notifications p-4">
                <BIconChatLeftFill variant="secondary" @click="$router.push({name:'chat'})"></BIconChatLeftFill>
            </div>
            <div class="notifications p-4">
                <BIconBellFill variant="secondary" @click="showNotif()"></BIconBellFill>
            </div>
            <div class="user-area pl-4 d-flex flex-nowrap align-items-center">

                <span class="m-0 h-50" style="font-size: 0.8vw;">{{ username }}</span>
                <!-- <img :src="require('../assets/logo.png')" class="profile-pic rounded-circle mx-3" alt=""> -->
                <b-avatar v-if="!profilePic" class="mx-3"></b-avatar>
                <img v-if="profilePic" :src="profilePic" class="profile-pic rounded-circle mx-3" alt="">
                
            </div>
            <div class="credits">
                <span v-if="getUser.role != 'freelance'">
                    ${{parseFloat(storeMoney)?.toFixed(2)}}
                </span>
                <span v-else>
                    <strong class="freelance-credits">{{ getUser.credits }} puntos</strong>
                </span>
            </div>
        </div>
    </div>
</template>
<script>
import { BIconBellFill, BIconChatLeftFill } from 'bootstrap-vue'
import { mapGetters,mapMutations } from 'vuex'

export default {
    props: [
        "username",
        "profilePic",
        "storeMoney",
    ],
    computed:{
        getStoreUrl(){
            return process.env.VUE_APP_STATIC_URL+'/store/'
        },
    ...mapGetters({
      notifications:'getNotifications',
      getUser:'getSelfUser'
    })
  },
    methods: {
        showNotif() {
            this.$refs["notification-modal"].show()
        },
        getNotificationsList() {
            
            this.$axios.get("api/notifications/")
                .then((res) => {
                    this.$store.commit("setNotifications", res.data.results)
                })
                .catch((err) => {
                    console.log(err.response)
                })
        },
        ...mapMutations(
      [
        "setNotifications"
      ]

    )
    },
    data() {
        return {
        }
    },
    mounted() {
        this.$setupAxios()
        this.getNotificationsList()
        
        
        
    },

    components: {
        BIconBellFill,
        BIconChatLeftFill
    }
}
</script>
<style>
.profile-pic {
    height: 100%;
    width: 40px;
}

.notifications>* {
    cursor: pointer;
}
.notification{
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 10px 10px 5px 10px;

}

.notification__type{
    font-size:12px;
    margin:0;
}
.notification__description{
    font-size:14px;
    margin:0;
}
.notification__created_at{
    font-size:10px;
    margin:10px 0px 0px 0px;
}

.user-area {
    border-left: solid 1px gray;
}
.freelance-credits{
    font-size: 12px;
    width:80px;
}
</style>