import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)

export default new Vuex.Store({
  state(){
    return{

      notifications:[],
      user_messages:[],
      self_user:{},
    }
  },
  getters: {
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
    setNotification(state, notf){
      state.notifications.push(notf)
    },
    setUserMessage(state, message){
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
      state.self_user = user
    }
  },
  actions: {
    retieveUser(context){
      this._vm.$setupAxios()
    
      this._vm.$axios.get("/api/same_user/")
      .then((res)=>{
        console.log(res.data.results)
        context.commit("setSelfUser", res.data.results[0])
      })
      .catch((err)=>{

        console.log(err)
      })
      

    }
  },
  modules: {
  }
})
