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
        <div class="col-md-8 d-flex align-items-center">
            <h5>{{ this.$route.meta.verbose_name }}</h5>
        </div>
        <div class="col-md-4 d-flex justify-content-center align-items-center" style="height: 40px;">
            <div class="notifications p-4">
                <BIconBellFill variant="secondary" @click="showNotif()"></BIconBellFill>
            </div>
            <div class="user-area pl-4 d-flex flex-nowrap align-items-center">

                <span class="m-0 h-50" style="font-size: 0.8vw;">{{ username }}</span>
                <!-- <img :src="require('../assets/logo.png')" class="profile-pic rounded-circle mx-3" alt=""> -->
                <img :src="profilePic" class="profile-pic rounded-circle mx-3" alt="">
            </div>
            <div class="credits">
                ${{parseFloat(storeMoney)?.toFixed(2)}}
            </div>
        </div>
    </div>
</template>
<script>
import { BIconBellFill } from 'bootstrap-vue'
export default {
    props: [
        "username",
        "profilePic",
        "storeMoney",
    ],
    methods: {
        showNotif() {
            this.$refs["notification-modal"].show()
        },
        getNotificationsList() {
            this.$axios.get("api/notifications/")
                .then((res) => {
                    this.notifications = [...res.data.results]
                })
                .catch((err) => {
                    console.log(err.response)
                })
        }
    },
    data() {
        return {
            notifications: []
        }
    },
    mounted() {
        this.$setupAxios()
        this.getNotificationsList()
        
    },

    components: {
        BIconBellFill
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
</style>