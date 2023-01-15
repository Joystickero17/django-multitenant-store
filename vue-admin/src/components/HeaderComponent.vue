<template>
    <div class="row m-0 p-3" style="height: 80px;">
        <div class="col-md-8 d-flex align-items-center">
            <h5>{{this.$route.meta.verbose_name}}</h5>
        </div>
        <div class="col-md-4 d-flex justify-content-center align-items-center" style="height: 40px;">
            <div class="notifications p-4">
                <BIconBellFill variant="secondary"></BIconBellFill>
            </div>
            <div class="user-area pl-4 d-flex flex-nowrap align-items-center">

                <span class="m-0 h-50" style="font-size: 0.8vw;">{{username}}</span>
                <!-- <img :src="require('../assets/logo.png')" class="profile-pic rounded-circle mx-3" alt=""> -->
                <img src="https://randomuser.me/api/portraits/men/76.jpg" class="profile-pic rounded-circle mx-3" alt="">
            </div>
            <div class="credits">
                $0.00
            </div>
        </div>
    </div>
</template>
<script>
import { BIconBellFill } from 'bootstrap-vue'
export default {
    props:[
        "username"
    ],

    data(){
        return {
            
        }
    },
    components:{
        BIconBellFill
    }
}
</script>
<style>
.profile-pic{
    height: 100%;
    width: 40px;
}
.notifications>*{
    cursor: pointer;
}
.user-area{
    border-left: solid 1px gray;
}

</style>