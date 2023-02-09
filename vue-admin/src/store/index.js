import Vue from 'vue'
import Vuex from 'vuex'



Vue.use(Vuex)

export default new Vuex.Store({
  state(){
    return{

      notifications:[],
      user_messages:[],
      self_user:{},
      store_options:{
        see_my_stats_only: false,        
        see_my_products_only:false,
        see_my_store_orders_only:false,
        see_only_my_contacts:false,
      }
    }
  },
  getters: {
    getStoreOptions(state){
      return state.store_options
    },
    getNotifications(state){
      return state.notifications
    },
    getUserMessages(state){
      return state.user_messages
    },
    getSelfUser(state){
      return state.self_user
    }
  },
  mutations: {
    setContactsVisibilityOption(state, opt){
      state.store_options.see_only_my_contacts = opt
    },
    setProductsVisibilityOption(state, opt){
      state.store_options.see_my_products_only = opt
    },
    setOrdersVisibilityOption(state, opt){
      state.store_options.see_my_store_orders_only = opt
    },
    setStatsVisibilityOption(state, opt){
      state.store_options.see_my_stats_only = opt
    },
    setNotification(state, notf){
      state.notifications.push(notf)
    },
    setUserMessage(state, message){
      let users_ids = state.user_messages.map((item)=>{return item.id})
      // console.log("Verificando si el user esta en a lista",users_ids, message.from_user, users_ids.includes(message.from_user))
      if (!users_ids.includes(parseInt(message.from_user))){
        state.user_messages.push({
          id:message?.from_user,
          email:message?.from_user_email,
          profile_img:message?.from_user_img,
          messages:[
            message
          ]
        })
      }
      state.user_messages.map((item)=>{
        
        if(item.id == message.from_user){

          item.messages.push(message)
        }
      })
      state.user_messages = state.user_messages.sort((one, other)=>{
        let date1 = one.messages.length ? new Date(one.messages[one.messages.length-1].created_at).getTime() : null
        let date2 = other.messages.length ? new Date(other.messages[other.messages.length-1].created_at).getTime() : null
        console.log("order",date1,date2)
        if (!(date2||date1)){
          return -1
        }
        if (!date2){
          return -1
        }
        if (!date1){
          return 1
        }
        if ( date1 > date2){
          return -1
        }
        if (date2 > date1){
          return 1
        }
        return 0
      })
    },
    setSendingUserMessage(state, message){
      state.user_messages.map((item)=>{
        
        if(item.id == message.to_user && message.from_user != message.to_user){

          item.messages.push(message)
        }
      })
    },
    setUserMessages(state, messages){
      if (!state.user_messages.length){
        state.user_messages = messages
      }else{
        state.user_messages.push(...messages)
      }
      },
    setNotifications(state, notf_array){
      state.notifications.push(...notf_array)
    },
    setSelfUser(state, user){
      console.log("updating User",user)
      state.self_user = user
    }
  },
  actions: {
    retieveUser({commit}){
      this._vm.$setupAxios()
    
      this._vm.$axios.get("/api/same_user/")
      .then((res)=>{
        console.log("dispatch user",res.data.results)
        commit("setSelfUser", res.data.results[0])
      })
      .catch((err)=>{

        console.log(err)
      })
      

    }
  },
  modules: {
  }
})
