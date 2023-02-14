<template>
  <div class="mx-3">
    <div @click="$router.push({ name: 'product.new' })" class="add__btn bg-success">
      <BIconPlus font-scale="3"></BIconPlus>
    </div>
    <b-modal ref="delete-modal" title="Seleccione el Campo a Filtrar">
      <div class="d-flex flex-column">
        <span class="text-center modal-text">Esta seguro que desea borrar el producto con ID {{
          selectedProductDelete
        }}</span>


      </div>
      <template #modal-footer="{ cancel }">
        <b-button @click="deleteProduct" class="my-2" variant="outline-danger" outline>Si</b-button>
        <b-button @click="cancel" variant="outline-dark" outline>No</b-button>
      </template>
    </b-modal>
    <b-modal ref="response-delete-modal">
      {{ responseDeleteProduct }}
    </b-modal>
    <b-modal ref="filter-modal" hide-footer title="Filtros">
      <div class="d-flex flex-column">
        <span class="text-center">Rango de Precio</span>
        <div class="d-flex justify-content-center my-3">
          <div class="d-flex flex-column align-items-center">

            <label for="" class="d-block text-center">Mínimo</label>
            <b-input type="number" min="0" v-model.number="min_price" class="w-75 d-inline-block"></b-input>
          </div>
          <div class="d-flex flex-column align-items-center">
            <label for="" class="d-block text-center">Máximo</label>
            <b-input type="number" min="0" v-model.number="max_price" class="w-75 d-inline-block"></b-input>
          </div>
        </div>

        <b-form-checkbox v-model="products_store_only" v-if="user.role == 'website_owner'" class="my-3">
          Ver solo productos de la tienda
        </b-form-checkbox>
        <b-button @click="searchProducts()">Filtrar</b-button>
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
          <b-form-input id="input-default" v-model="search" @input="searchProducts()"
            placeholder="Buscar"></b-form-input>
        </div>
      </div>
      <div class="col-3">
        <div class="filter d-flex">
          <div @click="showFilterModal()" class="order-filter mx-3 d-flex align-items-center pointer">

            <BIconFunnelFill variant="secondary"></BIconFunnelFill>
            <span class="mx-1 p-0">Filtros</span>
          </div>

        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="mt-3">
        <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="30"
          @input="searchProducts($event)"></b-pagination>
      </div>
    </div>
    <div class="row  overflow-scrollx m-2 products_table p-1">
      <div v-if="noResults" class="col-12 d-flex justify-content-center">
        <img class="w-25" :src="noResultsImg" alt="">
      </div>
      <SkeletonBootstrapLoader :loading="loading" :quantity="7"></SkeletonBootstrapLoader>
      <div v-for="item in items" :key="item.id" class="w-100 border rounded my-2 px-2 py-3 d-flex product__card">
        <div class="col-2 pointer" @click="showProductDetail(item.id)">
          <img :src="item?.thumbnail?.file || storeLogo" class="products_table__img rounded" alt="">
        </div>
        <div class="col-9 pointer" @click="showProductDetail(item.id)">
          <h5>{{ item.name }}</h5>
          <small>Unidades: {{ item.quantity }}</small>
          <span class="secondary mx-2">
            <b-badge class="mx-1" v-for="(category, index) in item?.category?.full_path" :key="index">
              {{ category }}
            </b-badge>
          </span>
          <p class=" text-justify mt-2 product__price">
            {{ item.price ? "$" + item.price : "Gratuito" }}
          </p>
          <p v-if="item.product_storage_details?.id">
            
            {{ item.product_storage_details?.region }}, {{ item.product_storage_details?.subregion }}<span v-if="item.product_storage_details?.city">{{ item.product_storage_details?.city }}</span>
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
        <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="30"
          @input="searchProducts($event)"></b-pagination>
      </div>
    </div>

  </div>
</template>

<script>
import { BIconFunnelFill, BIconPencilSquare, BIconTrashFill, BIconPlus } from 'bootstrap-vue'
import SkeletonBootstrapLoader from '@/components/SkeletonBootstrapLoader.vue'
import { mapGetters } from 'vuex'

export default {
  components: {

    SkeletonBootstrapLoader,
    BIconFunnelFill,
    BIconPencilSquare,
    BIconTrashFill,
    BIconPlus

  },
  data() {
    return {
      loading: true,
      storeLogo: '/static/img/no-photo.png',
      noResultsImg: '/static/img/no_results.svg',
      isBusy: false,
      selectedProductDelete: null,
      min_price: 0,
      max_price: 0,
      currentPage: 1,
      totalRows: 0,
      selectedFilter: '',
      search: '',
      responseDeleteProduct: '',
      items: []
    }
  },
  computed: {
    ...mapGetters({
      user: "getSelfUser",
      options: "getStoreOptions"
    }),
    noResults() {
      return !this.items.length && !!this.search && !this.loading
    },
    products_store_only: {
      get() {
        return this.options.see_my_products_only
      },
      set(value) {
        this.$store.commit("setProductsVisibilityOption", value)
      }
    }
  },
  methods: {
    showDeleteProduct(id) {
      this.$refs["delete-modal"].show()
      this.selectedProductDelete = id
    },
    deleteProduct() {
      if (!this.selectedProductDelete) {
        this.responseDeleteProduct = 'No se ha seleccionado ningún producto a borrar'
        this.$refs["response-delete-modal"].show()
        return
      }
      this.$axios.delete(`/api/store_product/${this.selectedProductDelete}`)
        .then((res) => {
          if (res.status == 204) {
            this.responseDeleteProduct = 'Producto Borrado con éxito'
          }

        })
        .catch((err) => {
          if (err.response.status == 404) {
            this.responseDeleteProduct = 'Producto no Encontrado'
          }
        })
        .finally((data) => {
          console.log(data)
          this.$refs["delete-modal"].hide()
          this.$refs["response-delete-modal"].show()
          this.searchProducts()
        })
    },
    editProductDetail(id) {
      this.$router.push({ name: "product.edit", params: { id: id } })
    },
    showProductDetail(id) {

      this.$router.push({ name: "product.detail", params: { id: id } })
    },
    showFilterModal() {
      this.$refs["filter-modal"].show()
    },
    searchProducts(page = 1) {
      this.items = []
      this.loading = true
      let extra_params = {
        products_store_only: this.products_store_only
      }
      if (this.min_price > 0) {
        extra_params.min_price = this.min_price
      }
      if (this.max_price > 0 && this.max_price > this.min_price) {
        extra_params.max_price = this.max_price
      }

      this.$axios.get("/api/store_product/", { params: { search: this.search, page: page, ...extra_params }, withCredentials: true })
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
    this.$axios.get("/api/store_product/")
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
.product__card {
  max-height: 190px;
}

.add__btn {
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

.products_table__img {
  width: 100%;
  height: 20vh;
  object-fit: cover;
}

.product__price {
  font-size: 20px;
}

.products_table__description {
  text-overflow: ellipsis;
  height: 100px;
  overflow: hidden;
}

.modal-text {
  font-size: 20px;
}

.pointer {
  cursor: pointer;
}
</style>