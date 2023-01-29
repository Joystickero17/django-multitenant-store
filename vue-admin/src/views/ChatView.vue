<template>
    <div class="mx-5 mr-5 rounded border p-0 chat row">

        <div class="col-4 d-flex flex-column m-0 p-0 conversations d-inline-block">
            <div v-for="user in messages" :key="user.id" :class="{'bg-light': user.id == currentUser}" class="w-100 border d-flex align-items-center p-2 users_messages" @click="selectUser(user.id)">
                <b-avatar :src="user.profile_img" size="3rem" class="d-inline-block m-2"></b-avatar>
                <div class="last_message w-75 d-inline-block">
                    <strong class="d-block">{{user.email}}</strong>
                    <span class="d-block">{{user.messages.slice(-1)[0]?.content}}</span>
                    <small v-if="user.messages.slice(-1)[0]">{{user.messages.slice(-1)[0]?.created_at | moment("DD-MM-YYYY h:mm:ss a")}}</small>
                </div>
            </div>
            
        </div>
        <div class="col-8 p-0">
            <div class="messages" ref="messages">
                <div v-if="!currentUser">
                    <h4>Selecciona una conversación para empezar el chat</h4>
                </div>
                <div v-if="currentUser">
                    <div 
                    v-for="message in current_messages" 
                    :key="message.id" 
                    :class="{
                        'w-100 mb-2 d-flex justify-content-left':self_user.id!=message.from_user,
                        'w-100 mb-2 d-flex justify-content-end':self_user.id==message.from_user
                        }">
                        <div :class="{
                            'border text-white rounded-pill message-1 px-3 pt-2 bg-dark w-50':self_user.id!=message.from_user,
                            'border rounded-pill message-1 px-3 pt-2 bg-light w-50':self_user.id==message.from_user
                        }">
                            <span class="d-block pb-1">{{ message.content }}</span>
                            <small class="message-1__created_at">{{ message.created_at | moment("DD-MM-YYYY h:mm:ss a") }}</small>
                        </div>
                    </div>
                    <!-- <div class="w-100 mb-2 d-flex justify-content-end">
                        <div class="border rounded-pill message-1 px-3 pt-2 bg-light w-50">
                            <span class="d-block pb-1">Cuenteme, en que puedo ayudarle</span>
                            <small class="message-1__created_at">28/01/2023</small>
                        </div>
                    </div> -->
                </div>
            </div>
            <div class="send_panel d-flex">

                <b-form-textarea v-model="message" class="col-11 message__send d-inline-block"></b-form-textarea>
                <b-button @click="sendMessage()" class="col-1"><BIconCursorFill></BIconCursorFill></b-button>
            </div>
        </div>
    </div>
</template>
<script>
import { BIconCursorFill } from 'bootstrap-vue';
import {mapGetters, mapMutations} from 'vuex'
export default {
    components:{
        BIconCursorFill
    },
    data(){
        return {
            currentUser: null,
            current_messages:[],
            message:''
        }
    },
    computed:{
        ...mapGetters({
            messages:"getUserMessages",
            self_user:"getSelfUser"
        })
    },
    methods:{
        sendMessage(){
            let data = {
                to_user: this.currentUser,
                from_user: this.self_user.id,
                content:this.message,
            }
            this.message=''
            this.$axios.post("api/message/", data)
            .then((res)=>{
                this.$store.commit("setSendingUserMessage", res.data)
            })
        },
        selectUser(id){
            this.currentUser = id
            this.messages.map((item)=>{
                if(item.id == this.currentUser){
                    this.current_messages = item.messages
                }
            })
            console.log("scrollHeigth", this.$refs["messages"].scrollHeight)
            if (this.$refs["messages"].scrollHeight){
                this.$refs["messages"].scrollTop = this.$refs["messages"].scrollHeight
            }
            // window.setInterval(()=>{
            //     }, 5000);
        },
        ...mapMutations([
            "setUserMessage",
            "setSendingUserMessage"
        ])
    },
    mounted(){
        this.$setupAxios()
        // this.$axios.get("api/user_messages/")
        // .then((res)=>{
        //     this.results = res.data.results
        // })
        // .catch((err)=>{
        //     console.log(err)
        // })
    }
}
</script>
<style>
.users_messages{
    cursor: pointer;
}
.message-1{
    font-size: 12px;
}
.messages{
    height: 65vh;
    padding: 10px;
    overflow-y: scroll;
}

.last_message > span, .last_message > small{
    font-size: 12px;
}
.chat{
    min-height: 75vh;
}
.conversations{
    overflow-y: scroll;
    height: 75vh;
}
</style>