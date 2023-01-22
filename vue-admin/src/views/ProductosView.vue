<template>
  <div class="mx-3">
    <div @click="$router.push({name:'product.new'})" class="add__btn bg-success">
      <BIconPlus font-scale="3"></BIconPlus>
    </div>
    <b-modal ref="delete-modal" hide-footer title="Seleccione el Campo a Filtrar">
      <div class="d-flex flex-column">
        <span class="text-center modal-text">Esta seguro que desea borrar el producto con ID {{ selectedProductDelete }}</span>
        
        <b-button class="my-2" variant="outline-danger" outline>Si</b-button>
        <b-button variant="outline-dark" outline>No</b-button>
      
      </div>
    </b-modal>
    <b-modal ref="filter-modal" hide-footer title="Seleccione el Campo a Filtrar">
      <div class="d-flex flex-column">
        <span class="text-center">Filtros</span>
      <b-form-group class="mx-5" label="Campos de Producto">
        <b-form-radio v-model="selectedFilter" name="some-radios" :value="null">Todos los campos</b-form-radio>
        <b-form-radio v-model="selectedFilter" name="some-radios" value="name">Nombre del Producto</b-form-radio>
      </b-form-group>
      </div>
    </b-modal>
    <div class="row border justify-content-between align-items-center rounded mx-2 px-2 py-3">
      <div class="col-9 d-flex">
        <div class="col-6">
          <h5>
            Todos los productos
          </h5>
          <small>total: {{ totalRows }}</small>
        </div>
        <div class="col-6 d-flex align-items-center">
          <b-form-input id="input-default" v-model="search" @input="searchProducts()" placeholder="Buscar"></b-form-input>
        </div>
      </div>
      <div class="col-3">
        <div class="filter d-flex">
          <div class="order-filter d-flex align-items-center pointer">

            <BIconFilter variant="secondary" ></BIconFilter>
            <span class="mx-1 p-0">Orden</span>
          </div>
          <div @click="showFilterModal()" class="order-filter mx-3 d-flex align-items-center pointer">

            <BIconFunnelFill variant="secondary" ></BIconFunnelFill>
            <span class="mx-1 p-0">Filtros</span>
          </div>
          
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
        <div class="mt-3">
      <b-pagination 
      v-model="currentPage" 
      :total-rows="totalRows"
      :per-page="30"
      @input="searchProducts($event)"
      ></b-pagination>
    </div>
      </div>
      <div class="row  overflow-scrollx m-2 products_table p-1">
        <div  v-if="noResults" class="col-12 d-flex justify-content-center">
          <img class="w-25" :src="noResultsImg" alt="">
        </div>
        <SkeletonBootstrapLoader :loading="loading" :quantity="7"></SkeletonBootstrapLoader>
        <div v-for="item in items" :key="item.id" class="col-12 border rounded my-2 px-2 py-3 d-flex">
          
          <div class="col-2 pointer" @click="showProductDetail(item.id)">
            <img :src="item?.thumbnail?.file || storeLogo" class="products_table__img rounded" alt="">
          </div>
          <div class="col-9 pointer" @click="showProductDetail(item.id)">
            <h5>{{ item.name }}</h5>
            <span class="secondary">
              <b-badge class="mx-1" v-for="(category,index) in item?.category?.full_path" :key="index">
                {{ category }}
              </b-badge>
          </span>
            <p class="products_table__description text-justify mt-2 product__price">
              {{ item.price ? "$"+item.price: "Gratuito"  }}
            </p>
          </div>
          <div class="col-1 d-flex">
            <div class="px-2 pointer" @click="editProductDetail(item.id)">
              <BIconPencilSquare></BIconPencilSquare>
            </div>
            <div class="px-2 pointer" @click="showDeleteProduct(item.id)">
              <BIconTrashFill></BIconTrashFill>
            </div>
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="mt-3">
      <b-pagination 
      v-model="currentPage" 
      :total-rows="totalRows"
      :per-page="30"
      @input="searchProducts($event)"
      ></b-pagination>
    </div>
      </div>
    
  </div>
</template>

<script>
import { BIconFilter,BIconFunnelFill,BIconPencilSquare,BIconTrashFill,BIconPlus } from 'bootstrap-vue'
import SkeletonBootstrapLoader from '@/components/SkeletonBootstrapLoader.vue'

export default {
  components: {
    BIconFilter,
    SkeletonBootstrapLoader,
    BIconFunnelFill,
    BIconPencilSquare,
    BIconTrashFill,
    BIconPlus
    
  },
  data() {
    return {
      loading:true,
      storeLogo: '/static/img/no-photo.png',
      noResultsImg:'/static/img/no_results.svg',
      isBusy: false,
      selectedProductDelete:null,
      currentPage:1,
      totalRows:0,
      selectedFilter:'',
      search:'',
      items: []
    }
  },
  computed:{
    noResults(){
      return !this.items.length && !!this.search && !this.loading
    }
  },
  methods: {
    showDeleteProduct(id){
      this.$refs["delete-modal"].show()
      this.selectedProductDelete = id
    },
    editProductDetail(id){
      this.$router.push({name:"product.edit",params:{id:id}})
    },
    showProductDetail(id){
      
      this.$router.push({name:"product.detail",params:{id:id}})
    },
    showFilterModal(){
      this.$refs["filter-modal"].show()
    },
    searchProducts(page=1){
      this.items = []
      this.loading = true
   this.$axios.get("/api/product/",{params:{search:this.search, page:page},withCredentials:true})
      .then((response) => { return response })
      .then((data) => {
        let results = data.data
        this.items = results.results
        this.totalRows = results.count
        this.loading = false
      })
      .catch((err) => { console.log(err) })
    }
  },
  mounted() {
    this.loading = true
   this.$axios.get("/api/product/")
      .then((response) => { return response })
      .then((data) => {
        let results = data.data
        this.items = results.results
        this.totalRows = results.count
        this.loading = false
      })
      .catch((err) => { console.log(err) })
  }
}
</script>
<style>
.add__btn{
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  bottom: 10px;
  right: 10px;
  z-index: 100;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  color: white;
  cursor: pointer;
}
.products_table {
  height: 80vh;
  overflow-y: scroll;

}
.products_table__img{
  width: 100%;
  height: 20vh;
  object-fit: cover;
}
.product__price{
  font-size: 20px;
}
.products_table__description{
  text-overflow: ellipsis;
  height: 100px;
  overflow: hidden;
}
.modal-text{
  font-size: 20px;
}
.pointer{
  cursor: pointer;
}
</style>