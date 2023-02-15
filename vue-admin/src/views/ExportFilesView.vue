<template>

    <div>
        <div class="row mx-5 mb-4">
            <div class="col-12">
                <b-table :items="items" :fields="fields">
                    <template #cell(file)="data">
                        <a class="btn btn-dark" :href="data.item.file">Descargar</a>
                    </template>
                </b-table>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            items: [],
            fields: [
                {
                    key: 's3_file_name',
                    label: "Nombre del Archivo",
                    sortable:true,

                },
                {
                    key: 'created_at',
                    label: "Fecha de Exportación",
                    sortable:true

                },
                {
                    key: 'file',
                    label: 'Descarga'
                },
            ]

        }
    }, methods: {
        getItems() {
            this.$axios.get("api/export_files",)
                .then((res) => {
                    this.items = res.data.results
                })
                .catch()
        }
    }, mounted() {
        this.getItems()
    }
}
</script>