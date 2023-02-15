<template>
  <div id="app">
    <audio ref="notification" :src="`@/assets/media/notification.mp3`"></audio>
    <div class="container-fluid">
      <div class="row flex-nowrap">
        <div class="col-2 bg-dark navigation__menu p-0 mr-4">
          <div class="store-logo mb-3 pt-3">
            <!-- <img :src="this.storeLogo" class="h-75 my-3" alt=""> -->
            <b-avatar class="mb-2" :src="this.storeLogo" size="8rem"></b-avatar>
            <h5 class="text-center"><a class="text-decoration-none text-white" :href="storeUrl">{{ storeName }}</a></h5>
          </div>

          <router-link v-if="getSelfUser.role != 'freelance'" activeClass="active" to="/" exact>Estadística</router-link>
          <router-link v-if="getSelfUser.role != 'freelance'" activeClass="active"
            to="/contacts">Contactos</router-link>
          <router-link v-if="getSelfUser.role != 'freelance'" activeClass="active"
            to="/freelancers-list">Freelancers</router-link>
          <router-link v-if="getSelfUser.role == 'freelance'" activeClass="active"
            to="/freelance-resume">Resumen</router-link>
          <router-link v-if="getSelfUser.role != 'freelance'" activeClass="active" to="/ventas">Órdenes</router-link>
          <router-link v-if="getSelfUser.role != 'freelance'" activeClass="active"
            to="/products">Productos</router-link>
          <router-link activeClass="active" :to="{name:'config'}">Configuración</router-link>
          <router-link activeClass="active" :to="{name:'export_files'}">Archivos Exportados</router-link>

        </div>
        <div class="p-0 w-100">

          <HeaderComponent :username="username" :profilePic="profilepicsrc" :storeMoney="storeMoney" />
          <router-view class="mt-5" />
          <vue-progress-bar></vue-progress-bar>
        </div>
      </div>
    </div>
    <nav>

    </nav>
  </div>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import HeaderComponent from './components/HeaderComponent.vue';
import {Howl} from 'howler';
// import store from '@/store';

// import axios from 'axios'

export default {
  components: {
    HeaderComponent
  },
  data() {
    return {
      storeUrl: '',
      storeLogo: '/static/img/no-photo.png',
      storeName: '',
      storeMoney: 0,
      username: '',
      profilepicsrc: '',
      notifications: [],
    }
  },
  methods: {
    ...mapMutations(
      [
        "setNotification",
        "setUserMessage",
        "setUserMessages",
        "setSelfUser"
      ]

    )
  },
  computed: {
    ...mapGetters([
      "getSelfUser"
    ])
  },
  mounted() {
    let sound = new Howl({
      src:[`${this.$baseStaticUrl}${require(`@/assets/media/notification.mp3`)}`]
    })
    
    this.$setupAxios()
    console.log(this.$store)
    this.$axios.get("api/user_messages/")
      .then((res) => {
        this.$store.commit("setUserMessages", res.data.results)
      })
    this.$axios.get("/api/same_user/", { withCredentials: true })
      .then((res) => { return res.data })
      .then((data) => {
        let user = data.results[0]
        this.$store.commit("setSelfUser", user)
        if (!user.store_details && user.role != 'freelance') {

          window.location.href = "/store/?user_has_no_store=true"
        }
        if (user.role == 'freelance') {
          this.$router.push({ name: "freelance.resume" })
        } else {
          this.storeUrl = `/store/${user.store_details?.slug}`
          this.storeName = user.store_details.name

          this.storeMoney = user.store_details.money
        }
        console.log(user.role != 'freelance')
        this.username = user.email
        if (user.name && user.last_name) {
          this.username = `${user.name} ${user.last_name}`
        } 
        if (user.role == "website_owner" && !user.store_details?.logo) {
          this.storeLogo = `${this.$baseStaticUrl}${require("@/assets/logo.png")}`
        } else {
          this.storeLogo = user.store_details?.logo || `${this.$baseStaticUrl}${require("@/assets/logo.png")}`
        }
        if (user.role == "website_owner" && !user.profile_img) {
          this.profilepicsrc = `${this.$baseStaticUrl}${require("@/assets/logo.png")}`
        } else {
          this.profilepicsrc = user.profile_img
        }

        let connection = new WebSocket(`${process.env.VUE_APP_WS_URL}ws/notifications/${user.store_details?.slug || user.id}/`);
        let _this = this
        connection.onmessage = (event) => {
          let res = JSON.parse(event.data)
          console.log(res)
          _this.$store.commit("setNotification", res)
          
          _this.$bvToast.toast(`${res.message}`, {
            title: 'Notificacion',
            autoHideDelay: 5000,
            appendToast: true
          })
          if (res.to_user) {
            console.log("sending Message")
            _this.$store.commit("setUserMessage", res)
            sound.play()
          }
          console.log(event.data)

        }

      })
  }
}
</script>
<style>
.store-logo {
  height: 180px;
  display: flex;
  justify-items: center;
  flex-direction: column;
}

.navigation__menu {
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

a,
a:hover {
  text-decoration: none;
  color: darkgray;

}

.navigation__menu>a {
  text-decoration: none;

  color: white;
  padding: 5px 0px 5px 0px;
  width: 100%;
  padding-top: 15px;
  padding-bottom: 15px;
  text-align: center;

}

.navigation__menu>a.active {
  background-color: gray;
  border-left: 2px solid white;
}

.navigation__menu>a:hover {
  text-decoration: none;
  color: darkgray;
}
</style>


