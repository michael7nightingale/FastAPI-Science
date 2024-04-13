<script>
import {getScienceList} from "/src/services/ScienceService";
import {buildStaticUrl} from "@/services/Base";

export default {
  name: "SciencesListView",
  methods: {buildStaticUrl},
  data(){
    return {
      sciences: []
    }
  },
  mounted() {
    let promise = getScienceList()
    promise.then(response => this.sciences = response)
    .then(() => {
       document.getElementById("loader").className = document.getElementById("loader").className.replace("show", "hide")
       document.getElementById("main").className = document.getElementById("main").className.replace("hide", "show")
    });
  }

}
</script>



<template>
<div class="centered show" id="loader">
  <span class="loader"></span>
</div>
<div class="hide" id="main">
  <div class="jumbotron">
      <h1>Раздел наук</h1>
  </div>

  <div class="row">
      <div class="col science-col" v-for="science in sciences" v-bind:key="science">
          <img :src="buildStaticUrl(`/sciences/${science.image_path}`)" style="width: 200px; height: 200px">
          <h2>{{ science.title }}</h2>
          <p>
              {{ science.content.slice(0, 50) }}
          </p>
          <router-link class="btn btn-outline-primary text" :to="{name: 'science', params: {slug: science.slug}}">перейти &raquo;</router-link>
      </div>
  </div>
</div>
</template>



<style scoped>
@import '../../assets/css/sciences.css';
</style>