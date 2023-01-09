<template>
    <div v-if="loading" class="w-100">
        <div v-for="item in quantity" :key="'skeleton'+item" class="col-12 d-flex border rounded mx-0 my-2 p-3"
            style="overflow:hidden; height: 150px">
            <div class="col-2">
                <b-skeleton-img></b-skeleton-img>
            </div>
            <div class="col-9">
                <b-skeleton animation="wave" width="85%"></b-skeleton>
                <b-skeleton animation="wave" width="55%"></b-skeleton>
                <b-skeleton animation="wave" width="70%"></b-skeleton>
                <b-skeleton animation="wave" width="85%"></b-skeleton>
                <b-skeleton animation="wave" width="55%"></b-skeleton>
                <b-skeleton animation="wave" width="70%"></b-skeleton>
            </div>
        </div>
    </div>

</template>
<script>
export default {
    props:[
        "loading",
        "quantity"
    ]
}
</script>