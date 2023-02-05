<template>
    <div class="container">
        <b-modal ref="success-gc">
            {{ gc_success_message }}

        </b-modal>
        <b-modal ref="error-gc">
            <p>Se encontraron los siguientes errores:</p>
            <ul>
                <li>{{ gc_error }}</li>
            </ul>

        </b-modal>
        <div class="row">
            <div class="col-md-3">
                <b-card>
                    <b-card-text>

                        <h6 class="text-center">Puntos</h6>
                        <h1 class="text-center">
                            <number ref="number1" :from="0" :to="user.credits" :duration="3" easing="Power1.easeOut" />
                        </h1>
                    </b-card-text>
                </b-card>

            </div>
            <div class="col-md-3">
                <b-card>
                    <b-card-text>

                        <h6 class="text-center">Asistencias</h6>
                        <h1 class="text-center">
                            <number ref="number1" :from="0" :to="12" :duration="3" easing="Power1.easeOut" />
                        </h1>
                    </b-card-text>
                </b-card>

            </div>
        </div>
        <div class="row p-3">
            <h4>Premios</h4>
            
        </div>
        <div class="row p-3">
            <div class="col-md-3">
        <b-card>
          <b-card-text>
            <div class="d-flex align-items-center justify-content-center flex-column">
                <h6 class="text-center mb-4">5$ Gift Card</h6>
                <img class="w-25" :src="`${this.$baseStaticUrl}${require('@/assets/amazon.svg')}`">
                <b-progress :max="5000" height="2rem" class="mt-2 w-100">
                <b-progress-bar :value="user.credits">
                    
                <span>progreso: <strong>{{ parseFloat(user.credits).toFixed(2) }} / {{ 5000 }}</strong></span>
                
                </b-progress-bar>
                </b-progress>
                <b-button v-if="user.credits == 5000" class="mt-2" @click="sendGC()">Retirar Gift Card</b-button>
            </div>
        </b-card-text>
        </b-card>
        
      </div>
        </div>

    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            gc_error:{},
            gc_success_message: '',
        }
    },
    methods:{
        showSuccessModal(){
            this.$refs["success-gc"].show()
        },
        showErrorModal(){
            this.$refs["error-gc"].show()
        },
        sendGC(){
            this.$axios.post("api/send_gc/")
            .then((res)=>{
                this.gc_success_message=res.data.message
                this.showSuccessModal()
                
            })
            .catch((err)=>{
                this.gc_error = err.response.data.message
                this.showErrorModal()
            })
            .finally((res)=>{
                console.log(res)
                this.$store.dispatch("retieveUser")
            })
        }
    },
    computed: {
        ...mapGetters({
            user: "getSelfUser"
        })
    },
    mounted(){
        this.$setupAxios()

    }
}
</script>