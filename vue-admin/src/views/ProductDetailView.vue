<template>
    <div class="mx-5">
        <a @click.prevent="returnToList()" href="#"><BIconArrowLeft></BIconArrowLeft> Regresar al listado</a>
        <div class="row border rounded p-3">
            <div class="col-lg-6">
                <h5 for="">N° de Producto</h5>
                <p>N° {{ product.id }}</p>
                <h5 for="">Nombre del Producto</h5>
                <p>{{ product.name }}</p>
                <h5 for="">Categorías</h5>
                <p>{{ product.category?.name }}</p>
                <div class="d-flex">

                    <div class="col-6">
    
                        <h6>¿Posee Existencias?</h6>
                        <p>{{ product.has_stock ? "Si" : "No" }}</p>
                        <div class="my-3">
                            <h6>Condición</h6>
                            <p>{{ product.verbose_condition }}</p>
                        </div>
                    </div>
                    <div class="col-6">
    
                        <h6>N° de Unidades</h6>
                        <p>{{ product.quantity }}</p>
                        <div class="my-3">
                            <h6>Precio</h6>
                            <p>{{ product.price }} USD</p>
                        </div>
                    </div>
                </div>
                <!-- <p>{{ product }}</p> -->
            </div>
            <br>
            <div class="col-lg-5">
                <h6>Fotos</h6>
                <div v-if="!selectedImageSrc" class="current-image d-flex justify-content-center align-items-center">
                    <b-spinner style="width: 3rem; height: 3rem;" label="Large Spinner" type="grow"></b-spinner>
                </div>
                <img :src="selectedImageSrc" v-if="!!selectedImageSrc" class="current-image rounded border" alt="">                
                <div class="col-12 d-flex">
    
                    <div @click="selectPhoto('thumbnail')" :class="{'border border-danger': selectedImage == 'thumbnail'}" class="tiny-image my-2">
                        <img :src="product.thumbnail || '/static/img/no-photo.png'" ref="thumbnail" class="w-100" alt="">
                    </div>
                    <div v-for="image in product.photos" @click="selectPhoto('photo-'+image.id)" :class="{'border border-danger': selectedImage == 'photo-'+image.id}" :key="'photo-'+image.id" class="tiny-image my-2">
                        <img :src="image.file || '/static/img/no-photo.png'" :ref="'photo-'+image.id" class="w-100" alt="">
                    </div>
                </div>
            </div>
        </div>
        <div class="row border rounded p-3 my-2">
            <div class="col-12">
                <h5>Descripción</h5>
                <p>
                    {{ product.description ? product.description :'Este Producto no posee Descripción, agrega una!' }}
                </p>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import { BIconArrowLeft } from 'bootstrap-vue'
export default {
    components:[
    BIconArrowLeft
    ],
    data(){
        return {
            product: {},
            selectedImage:'',
            selectedImageSrc:'',
        }
    },
    methods:{
        returnToList(){
            this.$router.push({name:"productos-list"})
        },
        selectPhoto(imageId){
            this.selectedImage = imageId
            let img_elem = this.$refs[imageId][0] || this.$refs[imageId]
            this.selectedImageSrc = img_elem.src
        }
    },
    mounted(){
        let id = this.$route.params.id
        
        axios.get(`/api/product/${id}`, {withCredentials:true})
        .then((res)=>res.data)
        .then((data)=>{
            this.product = data
            this.selectedImageSrc = this.product.thumbnail || '/static/img/no-photo.png'
        })
    }
}
</script>
<style scoped>
.tiny-image{
    width: 60px;
    height: 60px;
}
.tiny-image > img{
  width: 50px;
  height: 50px;
  
  object-fit: cover;
}
.current-image{
  width: 30vw;
  height: 300px;
  
  object-fit: cover;
}

</style>