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
    
  },
  modules: {
  }
})
