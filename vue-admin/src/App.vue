<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row flex-nowrap">
        <div class="col-2 bg-dark navigation__menu p-0 mr-4">
          <div class="store-logo">
            <img :src="this.storeLogo"  class="h-75" alt="">
            <h5 class="text-center"><a class="text-decoration-none text-white" :href="storeUrl">Tienda 1</a></h5>
          </div>
          <router-link activeClass="active" to="/" exact>Dashboard</router-link>
          <router-link activeClass="active" to="/contacts">Contactos</router-link>          
          <router-link activeClass="active" to="/freelancers">Freelancers</router-link>
          <router-link activeClass="active" to="/ventas">Ordenes</router-link>
          <router-link activeClass="active" to="/products">Productos</router-link>
          <router-link activeClass="active" to="/settings">Configuración</router-link>

        </div>
        <div class="p-0 w-100">
          
          <HeaderComponent :username="username"/>
          <router-view class="mt-5"/>
          <vue-progress-bar></vue-progress-bar>
        </div>
      </div>
    </div>
    <nav>
      
    </nav>
  </div>
</template>
<script>
import HeaderComponent from './components/HeaderComponent.vue';
// import axios from 'axios'

export default {
  components:{
    HeaderComponent
  },
  data(){
    return {
      storeUrl: '',
      storeLogo: '/static/img/no-photo.png',
      username:'',
    }
  },
  mounted(){
    this.$setupAxios()
    this.$axios.get("/api/same_user/", {withCredentials:true})
    .then((res)=>{return res.data})
    .then((data)=>{
      let user = data.results[0]
      if (!user.store_details){
        window.location.href="/store/?user_has_no_store=true"
      }
      this.username = user.email
      if (user.name && user.last_name){
        this.username = `${user.name} ${user.last_name}`
      }
      this.storeUrl = `/store/${user.store_details?.slug}`
      let connection = new WebSocket(`${process.env.WEBSOCKET_URL}/ws/notifications/${user.store_details.slug}/`);
      let _this = this
      connection.onmessage = (event) => {
        let res = JSON.parse(event.data)
        _this.$bvToast.toast(`${res.message}`, {
          title: 'Notificacion',
          autoHideDelay: 5000,
          appendToast: true
        })
        console.log(event.data)
      }
      this.storeLogo = user.store_details?.logo || '/static/img/no-photo.png'
    })
  }
}
</script>
<style>
.store-logo{
  height: 150px;
}
.navigation__menu{
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}
a, a:hover{
  text-decoration: none;
  color: darkgray;

}
.navigation__menu > a{
  text-decoration: none;
  
  color: white;
  padding: 5px 0px 5px 0px;
  width: 100%;
  padding-top: 15px;
  padding-bottom: 15px;
  text-align: center;
  
}
.navigation__menu > a.active{
  background-color: gray;
  border-left: 2px solid white;
}

.navigation__menu > a:hover{
  text-decoration: none;
  color: darkgray;
}
</style>


