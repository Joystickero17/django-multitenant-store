<template>
    <div class="mx-5">

        <div class="row my-5 justify-content-center">
            <div class="col-6">
                <div class="mb-3">
                    <label for="">Tipo de Almacén</label>
                    <b-select :state="!errors.storage_type" :options="storage_options" v-model="storage_type"></b-select>
                    <small class="text-danger">{{ errors.storage_type }}</small>
                </div>
                <div class="mb-3">
                    <label for="">Estado</label>
                    <b-select :state="!errors.region" @input="getSubRegion" :options="regions" v-model="region"></b-select>
                    <small class="text-danger">{{ errors.region }}</small>
                </div>
                <div class="mb-3">
                    <label for="">Municipio</label>
                    <b-select :state="!errors.subregion" @input="getCities" :options="subregions" v-model="subregion"></b-select>
                    <small class="text-danger">{{ errors.subregion }}</small>
                </div>
                <div class="mb-3" v-if="cities.length">
                    <label for="">Ciudad</label>
                    <b-select :options="cities" v-model="city"></b-select>
                </div>
                <div class="mb-3">
                    <b-button @click="saveStorage" variant="success">Guardar</b-button>
                </div>
                
            </div>
            <div class="col-6">
                <div class="mb-3">
                    <small class="font-weigth-bold text-danger">{{ this.errors.mapa }}</small>
                    <label for="">Coordenadas</label>
                    <vl-map @click="selectPoint" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
                        style="height: 200px">
                        <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

                        <vl-layer-tile id="osm">
                            <vl-source-osm></vl-source-osm>
                        </vl-layer-tile>
                        <vl-feature v-if="point">
                            <vl-geom-point :coordinates="point"></vl-geom-point>
                        </vl-feature>
                    </vl-map>
                </div>
                <strong class="mx-3"><small>Latitud: {{ parseFloat(center[1]).toFixed(2) }}</small></strong>
                <strong class="mx-3"><small>Longitud: {{ parseFloat(center[0]).toFixed(2) }}</small></strong>
                <strong class="mx-3"><small>Zoom: {{ parseFloat(zoom).toFixed(2) }}</small></strong>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            storage_options: [
                { value: 'tienda_fisica', text: 'Tienda Física' },
                { value: 'almacen', text: 'Almacén' }
            ],
            regions: [],
            subregions: [],
            cities: [],
            storage_type:'',
            city: '',
            region: '',
            subregion: '',
            center: [0, 0],
            rotation: 0,
            address: '',
            zoom: 0,
            errors: {},
            point: null,
            modal_errors:[]
        }
    },    
    methods: {
        selectPoint(e) {
            console.log(e.coordinate)

            this.point = e.coordinate
        },
        searchCoordinates() {
            let data = {
                country: 'venezuela'
            }
            this.zoom = 5
            if (this.region.length) {
                data.state = this.region
                this.zoom = 7
            }
            if (this.subregion.length) {
                data.county = this.subregions.find((item)=>{return this.subregion == item.value})?.search_name
                this.zoom = 10
            }
            this.$axios.get("https://nominatim.openstreetmap.org/search", { params: { ...data, format: "json" } })
                .then((res) => {
                    let data = res.data[0]
                    console.log(data.lat, data.lon)
                    this.center = [parseFloat(data.lon), parseFloat(data.lat)]
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        getSelectableRegions(api_response) {
            if (!api_response) return
            let result = []
            api_response.map((item) => {
                result.push({ value: item.name_ascii, text: item.name, search_name: item.name_ascii.replace("Municipio ","").replace("Autonomo ","") })
            })
            return result
        },
        getRegions() {
            this.subregions = []
            this.subregion = ''
            this.cities = []
            this.city = ''
            this.$axios.get("api/regions")
                .then((res) => {
                    this.regions = this.getSelectableRegions(res.data.results)
                    this.searchCoordinates()
                })
                .catch(err => console.log(err))
        },
        getSubRegion() {
            
            if (!this.region.length) return
            this.$axios.get("api/subregions/", { params: { region: this.region } })
                .then((res) => {
                    this.cities = []
                    this.city = ''
                    this.subregions = this.getSelectableRegions(res.data.results)
                    this.searchCoordinates()
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        getCities() {
            
            if (!this.subregion.length) {
                return
            }
            this.$axios.get("api/cities/", { params: { subregion: this.subregion } })
                .then((res) => {
                    this.searchCoordinates()
                    if (res.data.count == 0) {
                        return
                    }
                    this.cities = this.getSelectableRegions(res.data.results)
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        checkForm() {
            this.errors = {}
            let valid = true
            if (!this.storage_type.length) {
                this.errors = { ...this.errors, storage_type: 'Este campo es requerido' }
                valid = false
            }
            if (!this.region.length) {
                this.errors = { ...this.errors, region: 'Este campo es requerido' }
                valid = false
            }
            if (!this.subregion.length) {
                this.errors = { ...this.errors, subregion: 'Este campo es requerido' }
                valid = false
            }
            if (!this.point){
                this.errors = { ...this.errors, mapa: 'Debe seleccionar un punto en el mapa para indicar la ubicación de su almacén' }
                valid = false
            }
            return valid
        },
        saveStorage() {
            if (!this.checkForm()) return

            let data = {
                coordinate_x: this.point[0],
                coordinate_y:this.point[1],
                zoom: this.zoom,
                region: this.region,
                subregion: this.subregion,
                city:this.city
            }
            this.$axios.post("api/product_storage/", data)
            .then((res)=>{
                console.log(res)
                this.$router.push({name:'config.storages'})
            })
            .catch((err)=>{
                if (err.response.status == 500){
                    this.modal_errors.push("Ha ocurrido un error inesperado")
                }
                if (err.response.data.message){
                    this.modal_errors.push(err.response.data.message)
                }
            })
        }
    },
    mounted() {
        this.$setupAxios()
        this.getRegions()
        this.searchCoordinates()
    }
}
</script>