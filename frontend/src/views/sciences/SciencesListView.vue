<script>
import {getScienceList} from "/src/services/ScienceService";

export default {
  name: "SciencesListView",
  data(){
    return {
      sciences: []
    }
  },
  mounted() {
    let promise = getScienceList()
    promise.then(response => this.sciences = response);
  }

}
</script>



<template>
<div class="jumbotron">
    <h1>Раздел наук</h1>
</div>

<div class="row">
    <div class="col science-col" v-for="science in sciences" v-bind:key="science">
        <img :src="`http://127.0.0.1:8001/static/sciences/${science.image_path}`" style="width: 200px; height: 200px">
        <h2>{{ science.title }}</h2>
        <p>
            {{ science.content.slice(0, 50) }}
        </p>
        <router-link class="btn btn-outline-primary text" :to="{name: 'science', params: {slug: science.slug}}">перейти &raquo;</router-link>
    </div>

</div>
</template>



<style scoped>
@import '../../assets/css/sciences.css';
</style>