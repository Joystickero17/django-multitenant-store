<template>

    <div class="mx-5">
        <b-modal ref="response-modal" size="md" title="Mensaje">{{ response_message }}</b-modal>

        <b-modal ref="category-modal" size="md" title="Seleccion de Categoría y Marca">
            <div class="col-12 d-flex flex-column align-items-center">

                <p>Seleccion: <b-badge class="mx-1" v-for="(category, index) in categoryRoute" :key="index"> {{
                    category
                }}</b-badge> <b-button @click="resetCategoryRoute()" pill size="sm">x</b-button></p>
                <b-input @input="browseCategory()" v-model="categorySearch" placeholder="buscar categoría"></b-input>


                <div class="image-upload-container mt-3">
                    <button class="btn btn-outline-danger m-1" @click="setAndSearchCategory(category)"
                        v-for="(category, index) in categories" :key="index">{{ category.name }}</button>
                </div>

            </div>
        </b-modal>
        <b-modal ref="brand-modal" size="md" title="Seleccion de Categoría y Marca">
            <div class="col-12 d-flex flex-column align-items-center">

                <p>Seleccion: <b-badge class="mx-1" v-if="selectedBrand"> {{ selectedBrand?.name }}</b-badge> <b-button
                        v-if="selectedBrand" @click="resetBrand()" pill size="sm">x</b-button></p>
                <b-input @input="browseBrand()" v-model="brandSearch" placeholder="buscar Marca"></b-input>


                <div class="image-upload-container mt-3">
                    <button class="btn btn-outline-primary m-1" @click="setAndSearchBrand(brand)"
                        v-for="(brand, index) in brands" :key="index">{{ brand.name }}</button>
                </div>

            </div>
        </b-modal>
        <div class="p-3 fixed-alert d-flex align-items-center">

            <b-button @click="submitChanges()" variant="primary" class="p-2">Guardar Cambios</b-button>
        </div>
        <div class="row border rounded p-3">

            <div class="col-lg-6">
                <h5 for="">N° de Producto</h5>
                <p>N° {{ newproduct.id }}</p>
                <h5 for="">Nombre del Producto</h5>
                <b-input @input="dataChanged" v-model="newproduct.name">

                </b-input>
                <div class="d-flex align-items-center mt-4">
                    <div class="col-6">
                        <div class="d-flex">
                            <h5 for="">Categorías </h5>
                            <a @click.prevent="changeCategoryBrand()" href="#" class="mx-2 mb-1">cambiar</a>
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
                            <a @click.prevent="changeBrand()" href="#" class="mx-2 mb-1">cambiar</a>
                        </div>
                        <b-badge>{{ newproduct.brand?.name }}</b-badge>
                    </div>
                </div>
                <div class="d-flex align-items-center mt-4">
                    <div class="col-12">
                        <h6>Precio (USD)</h6>
                        <b-form-input v-model="newproduct.price" :min="0" type="number"></b-form-input>
                    </div>
                </div>


                <div class="d-flex mt-4">

                    <div class="col-6">
                        <div>
                            <h6>Condición</h6>
                            <b-form-select v-model="newproduct.condition" :options="conditionOptions"
                                size="md"></b-form-select>
                        </div>
                    </div>
                    <div class="col-6">

                        <h6>N° de Unidades</h6>
                        <b-form-input v-model="newproduct.quantity" :min="0" type="number">

                        </b-form-input>

                    </div>
                </div>
                <div class="d-flex mt-4">

                    <div class="col-12">

                        <h5>Descripción</h5>
                        
                        <froala :tag="'textarea'" :config="config" v-model="newproduct.description">Init text</froala>
                        <!-- <b-form-textarea v-model="newproduct.description"
                            placeholder="La descripcion de tu producto debe ser llamativa!" rows="12" size="sm"
                            max-rows="12"></b-form-textarea> -->

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

                    <!-- <div @click="selectPhoto('thumbnail')"
                        :class="{ 'border border-danger': selectedImage == 'thumbnail' }" class="tiny-image my-2">
                        <img :src="product.thumbnail || '/static/img/no-photo.png'" ref="thumbnail" class="w-100"
                            alt="">
                    </div> -->
                    <div v-for="image in images" @click="selectPhoto('photo-' + image.id)"
                        :class="{ 'border border-danger': selectedImage == 'photo-' + image.id }"
                        :key="'photo-' + image.id" class="tiny-image ml-2 my-2">
                        <img :src="image.file || '/static/img/no-photo.png'" :ref="'photo-' + image.id" class="w-100"
                            alt="">
                    </div>
                </div>
                <div class="d-flex flex-column align-items-center">

                    <image-uploader :debug="1" :maxWidth="512" :quality="0.7" :autoRotate=true outputFormat="verbose"
                        :preview=false :className="['d-none']" :capture="false" accept="video/*,image/*"
                        doNotResize="['gif', 'svg']" @input="setImage">
                        <label for="fileInput" slot="upload-label" class="btn btn-outline-danger">
                            <figure class="text-center">
                                <BIconCloudUpload font-scale="3"></BIconCloudUpload>
                            </figure>
                            <span>Click para subir imagen</span>

                        </label>
                    </image-uploader>
                    <b-overlay :show="loadingImage" rounded="sm">

                        <div class="image-upload-container">
                            <draggable v-model="images" group="people">
                                <div v-for="(image, index) in images" :key="image.id"
                                    class="col-12 border rounded d-flex align-items-center my-2"
                                    :class="{ 'border border-danger': index == 0 }">

                                    <div class="tiny-image m-2">

                                        <img :src="image.file" alt="">
                                    </div>
                                    <p class="no-mp mx-4">{{ image.name }}</p>
                                    <small v-if="index == 0" class="main-image-text">Imagen Principal (miniatura)</small>
                                    <div class="close-btn" @click="removeImage(image.id)">

                                        <BIconXLg font-scale=".5"></BIconXLg>
                                    </div>
                                </div>
                            </draggable>
                        </div>
                    </b-overlay>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import ImageUploader from 'vue-image-upload-resize'
import { BIconCloudUpload, BIconXLg } from 'bootstrap-vue'
import draggable from 'vuedraggable'
// import axios from 'axios'
export default {
    components: {
        ImageUploader,
        BIconCloudUpload,
        // eslint-disable-next-line
        BIconXLg,
        draggable
    },
    data() {
        return {
            config: {
                placeholderText: 'Edit Your Content Here!',
                charCounterCount: false
            },
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
                    this.selectedImageSrc = res.data.file
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
            if (!this.images.length){
                this.selectedImageSrc = '/static/img/no-photo.png'
            }
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
            this.$axios.put(`/api/product/${this.product.id}/`, this.newproduct, { withCredentials: true })
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

        this.$axios.get(`/api/product/${id}`, { withCredentials: true })
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