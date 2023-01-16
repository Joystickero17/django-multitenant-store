<template>
    <div>
        <b-table :fields="fields">

        </b-table>
    </div>
</template>
<script>
export default {    
    data(){
        return {
            fields:["N°", "Método de Pago"],
            items:[],
        }
    }
    
}
</script>