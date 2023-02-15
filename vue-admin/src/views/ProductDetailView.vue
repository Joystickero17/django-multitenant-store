<template>

    <div class="mx-5 mb-3">
        <b-button class="my-1" squared variant="outline-danger" @click="$router.push({ name: 'productos-list' })">
            <BIconArrowBarLeft></BIconArrowBarLeft> Regresar al listado
        </b-button>
        <div class="row border rounded p-3">
            <div class="col-lg-6">
                <h5 for="">N° de Producto</h5>
                <p>N° {{ newproduct.id }}</p>
                <h5 for="">Nombre del Producto</h5>
                <p>{{ newproduct.name }}</p>


                <div class="d-flex align-items-center mt-4">
                    <div class="col-6">
                        <div class="d-flex">
                            <h5 for="">Categorías </h5>

                        </div>
                        <div class="d-flex ">
                            <div v-if="!!categoryRoute.length">
                                <b-badge class="mx-1" v-for="(category, index) in categoryRoute" :key="index"> {{
                                    category
                                }}</b-badge>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="d-flex">
                            <h5 for="">Marca </h5>

                        </div>
                        <b-badge>{{ newproduct.brand?.name }}</b-badge>
                    </div>
                </div>
                <div class="d-flex align-items-center mt-4">
                    <div class="col-12">
                        <h6>Precio (USD)</h6>
                        <p>{{ product.price }}</p>
                    </div>
                </div>
                <div class="d-flex mt-4">
                    <div class="col-6">
                        <div>
                            <h6>Condición</h6>
                            <p>{{ product.verbose_condition }}</p>
                        </div>
                    </div>
                    <div class="col-6">
                        <h6>N° de Unidades</h6>
                        <p>{{ product.quantity }}</p>
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
                    <div v-for="image in images" @click="selectPhoto('photo-' + image.id)"
                        :class="{ 'border border-danger': selectedImage == 'photo-' + image.id }"
                        :key="'photo-' + image.id" class="tiny-image ml-2 my-2">
                        <img :src="image.file || '/static/img/no-photo.png'" :ref="'photo-' + image.id" class="w-100"
                            alt="">
                    </div>
                </div>
            </div>
            <div class="d-flex flex-column mt-4">
                <div class="col-12">
                    <h5>Descripción</h5>
                    <div class="my-4" v-html="product.description"></div>
                </div>

            </div>
        </div>
        <div v-if="product.product_storage" class="row border rounded p-3 my-3">
            <div class="col-12">
                <h5>Almacén</h5>
                <b-table :items="[product.product_storage_details]" :fields="[
                    {
                        key: 'storage_type',
                        label: 'Tipo',
                    },
                    {
                        key: 'store',
                        label: 'Tienda'
                    },
                    {
                        key: 'region',
                        label: 'Estado'
                    },
                    {
                        key: 'subregion',
                        label: 'Municipio'
                    },
                    {
                        key: 'city',
                        label: 'Ciudad'
                    }
                ]">
            <template #cell(storage_type)="data">
                {{ data.item.storage_type == 'tienda_fisica' ? 'Tienda Física' : "Almacén" }}
            </template>    
            <template #cell(store)="data">
                <a class="text-primary" :href="getApiUrl+'store/'+data.item.store_details.slug">{{data.item.store_details.name}}</a>
            </template>    
            </b-table>
            </div>
        </div>
    </div>
</template>
<script>

import { BIconXLg, BIconArrowBarLeft } from 'bootstrap-vue'

// import axios from 'axios'
export default {
    components: {
        // eslint-disable-next-line
        BIconXLg,
        BIconArrowBarLeft,

    },
    data() {
        return {
            // Brands
            brands: [],
            selectedBrand: null,
            brandSearch: '',
            // Category
            categorySearch: '',
            categoryRoute: [],
            selectedCategory: null,
            categories: [],
            response_message: '',
            product: {},
            newproduct: {},
            initial_images_len: 0,
            initial_images: [],
            images: [],
            selectedImage: '',
            selectedImageSrc: '',
            loadingImage: false,
            conditionOptions: [
                {
                    value: "NEW",
                    text: "Nuevo"
                },
                {
                    value: "USED",
                    text: "Usado"
                },
                {
                    value: "REFURBISHED",
                    text: "Remanufacturado"
                }
            ]
        }
    },
    computed:{
        getApiUrl(){
            return process.env.VUE_APP_API_URL
        }
    },
    methods: {
        populateData(data) {
            this.images = []
            this.product = data
            this.images.push(...data.photos)
            this.initial_images_len = this.images.length
            this.initial_images = [...this.images]
            this.newproduct = JSON.parse(JSON.stringify(data));
            this.categoryRoute = this.newproduct.category?.full_path
            this.product.category_id = this.product.category?.id
            this.newproduct.category_id = this.product.category?.id
            this.product.brand_id = this.product.brand?.id
            this.newproduct.brand_id = this.product.brand?.id

            this.selectedImageSrc = this.product?.thumbnail?.file || this.images[0]?.file || require('@/assets/no-photo.png')
        },
        setAndSearchBrand(brand) {
            this.selectedBrand = brand
            this.newproduct.brand_id = brand.id
            this.browseBrand()
        },
        resetBrand() { },
        browseBrand() {
            let params = { search: this.brandSearch }
            this.$axios.get("/api/brand/", { params: params })
                .then((res) => {
                    this.brands = res.data.results
                })
                .catch((err) => {
                    console.log(err.response.data)
                })
        },
        resetCategoryRoute() {
            this.categoryRoute = this.product.category?.full_path
            this.selectedCategory = this.product.category?.id
            this.newproduct.category_id = this.product.category?.id
            this.selectedCategory = null
            this.browseCategory()
        },
        setAndSearchCategory(category) {
            this.selectedCategory = category.id
            this.newproduct.category_id = category.id
            this.categoryRoute = category.full_path
            this.browseCategory()
        },
        browseCategory() {
            let params = this.selectedCategory ? { search: this.categorySearch, parent: this.selectedCategory } : { search: this.categorySearch, parents_only: true }
            this.$axios.get("/api/category/", { params: params })
                .then((res) => {
                    this.categories = res.data.results
                })
                .catch((err) => {
                    console.log(err.response.data)
                })
        },
        setImage(file) {
            this.loadingImage = true
            this.$axios.post("/api/media/", {
                name: file.info.name,
                file: file.dataUrl

            })
                .then((res) => {
                    this.images.push({
                        id: res.data.id,
                        name: res.data.name,
                        file: res.data.file
                    })
                    this.loadingImage = false
                })
                .catch((err) => {

                    console.log(err)
                })

        },
        selectPhoto(imageId) {
            this.selectedImage = imageId
            let img_elem = this.$refs[imageId][0] || this.$refs[imageId]
            this.selectedImageSrc = img_elem.src
        },
        dataChanged() {
            console.log(JSON.stringify(this.product))
            console.log(JSON.stringify(this.newproduct))
            console.log(JSON.stringify(this.product) === JSON.stringify(this.newproduct))
        },
        changeCategoryBrand() {
            this.browseCategory()
            this.$refs["category-modal"].show()
        },
        changeBrand() {
            this.browseBrand()
            this.$refs["brand-modal"].show()
        },
        removeImage(id) {
            this.images = this.images.filter((item) => {
                return item.id !== id
            })
        },
        checkForm() {
            return true
        },
        submitChanges() {
            for (let index = 0; index < this.images.length; index++) {
                this.images[index] = { ...this.images[index], priority: index };

            }
            this.images[0] = { ...this.images[0], is_thumbnail: true }
            this.newproduct.photos = this.images
            console.log(JSON.stringify(this.newproduct, null, 4))
            this.$axios.put(`/api/store_product/${this.product.id}/`, this.newproduct, { withCredentials: true })
                .then((res) => {
                    console.log(res)
                    this.response_message = 'Producto Actualizado con éxito!'
                    this.$refs["response-modal"].show()
                    this.populateData(res.data)
                    this.$route.go()
                })
                .catch((err) => {
                    let message = err.response.status == 500 ? "Ha ocurrido un error inesperado" : err.response.data
                    this.response_message = message
                    this.$refs["response-modal"].show()
                })
        },
    },
    mounted() {

        let id = this.$route.params.id

        this.$axios.get(`/api/store_product/${id}`, { withCredentials: true })
            .then((res) => res.data)
            .then((data) => {
                this.populateData(data)
            })
    }
}
</script>
<style scoped>
.main-image-text {
    color: rgb(222, 0, 0);
    font-size: 10px;
}

.main-image {
    border: 0.8px solid rgb(222, 0, 0)
}

.close-btn {
    position: absolute;
    top: 0;
    right: 10px;
}

.image-upload-container {
    overflow-y: scroll;
    height: 200px;
    width: 350px;
    border: 0.8px solid rgb(203, 203, 203);
    padding: 20px;
}

.no-mp {
    margin: 0;
    padding: 0
}

.tiny-image {
    width: 50px;
    height: 50px;
}

.tiny-image>img {
    width: 50px;
    height: 50px;

    object-fit: cover;
}

.current-image {
    width: 30vw;
    height: 300px;

    object-fit: cover;
}

.fixed-alert {
    position: fixed;
    bottom: 10px;
    right: 10px;
    justify-content: right;
    height: 50px;
    z-index: 100;
    width: 250px;
    color: white;
}
</style>