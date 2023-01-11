<template>
    <div class="mx-5">
        <div v-if="!(JSON.stringify(product) === JSON.stringify(newproduct))" class="p-3 fixed-alert rounded border d-flex align-items-center">
                <p class="pt-3">Tienes cambios sin Guardar!</p>
        </div>
        <div class="row border rounded p-3">
            
            <div class="col-lg-6">
                <h5 for="">N° de Producto</h5>
                <p>N° {{ newproduct.id }}</p>
                <h5 for="">Nombre del Producto</h5>
                <b-input @input="dataChanged" v-model="newproduct.name">

                </b-input>
                <div class="d-flex align-items-center mt-4">
                    
                    <h5 for="">Categorías </h5>
                    <a @click.prevent="changeCategory()" href="#" class="mx-2 mb-1">cambiar</a>
                </div>
                <div class="d-flex ">
                    <p>{{ newproduct.category?.name }}</p> 
                </div>
                
                <div class="d-flex mt-4">

                    <div class="col-6">
                        <div>
                            <h6>Condición</h6>
                            <b-form-select v-model="newproduct.condition" :options="conditionOptions" size="md"></b-form-select>
                        </div>
                    </div>
                    <div class="col-6">
    
                        <h6>N° de Unidades</h6>
                        <b-form-input v-model="newproduct.quantity" type="number">

                        </b-form-input>
                        <div class="my-3">
                            <h6>Precio (USD)</h6>
                            <b-form-input v-model="newproduct.price" type="number"></b-form-input>
                            
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
                <b-form-textarea
                    
                    v-model="product.description"
                    placeholder="La descripcion de tu producto debe ser llamativa!"
                    rows="3"
                    max-rows="6"
                ></b-form-textarea>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data(){
        return {
            product: {},
            newproduct: {},
            selectedImage:'',
            selectedImageSrc:'',
            conditionOptions:[
                {
                    value:"NEW",
                    text:"Nuevo"
                },
                {
                    value:"USED",
                    text:"Usado"
                },
                {
                    value:"REFURBISHED",
                    text:"Remanufacturado"
                }
            ]
        }
    },
    methods:{
        selectPhoto(imageId){
            this.selectedImage = imageId
            let img_elem = this.$refs[imageId][0] || this.$refs[imageId]
            this.selectedImageSrc = img_elem.src
        },
        dataChanged(){
            console.log(JSON.stringify(this.product))
            console.log(JSON.stringify(this.newproduct))
            console.log(JSON.stringify(this.product) === JSON.stringify(this.newproduct))
        },
        changeCategory(){

        }
    },
    mounted(){
        let id = this.$route.params.id
        
        axios.get(`/api/product/${id}`, {withCredentials:true})
        .then((res)=>res.data)
        .then((data)=>{
            this.product = data
            this.newproduct = JSON.parse(JSON.stringify(data));
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
.fixed-alert{
    position: fixed;
    bottom: 10px;
    right: 10px;
    
    height: 50px;
    z-index: 100;
    width: 500px;
    color:white;
    background-color: brown;
}

</style>