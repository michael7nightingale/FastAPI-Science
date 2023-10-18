<script>
import {getCategoryDetail} from "/src/services/ScienceService";
import VueMathjax from 'vue-mathjax';


export default {
  name: "CategoryDetailView",
  components: {
    'VueMathjax': VueMathjax
  },
  data(){
    return {
      science: {slug: 'ps'},
      formulas: null,
      category: {},
      loaded: false
    }
  },
  mounted() {
    let promise = getCategoryDetail(this.$route.params.slug)
    promise.then(response => {
      this.category = response.category;
      this.formulas = response.formulas;
      this.science = response.science;
      this.loaded = true;
    })
    .then(() => {
       document.getElementById("loader").className = document.getElementById("loader").className.replace("show", "hide")
       document.getElementById("main").className = document.getElementById("main").className.replace("hide", "show")
    });
  },

}
</script>


<template>
<div class="centered show" id="loader">
  <span class="loader"></span>
</div>
<div class="hide" id="main">
<div class="jumbotron">
    <div id="faq">
     <ul>
       <li>
         <input type="checkbox" checked>
         <h2 align="center" style="text-align: center">{{ category.title }}</h2>
       <p class="lead">{{ category.content }}</p>
       </li>
     </ul>
    </div>
   <router-link :to="{name: 'science', params: {slug: science.slug}}" class="btn btn-primary btn-large">назад к {{ science.title }} &raquo;</router-link>
</div>
<div class="formulas" v-if="loaded">
  <div class="row">
    <div class="col" style="background-color: white">
      <ul>
          <h4 align="center">Содержание</h4>
              <li v-for="formula in formulas" v-bind:key="formula">
              <router-link class="" :to="{name: 'formula', params: {slug: formula.slug}}">
                   <p class="">{{ formula.title }}</p>
               </router-link>
              </li>
      </ul>

      </div>
    <div class="col">
      <div class="row" v-for="rowIdx in Array(Math.floor(formulas.length/3) + 1).keys()" v-bind:key="rowIdx">
          <div class="col" v-for="colIdx in Array(3).keys()" v-bind:key="colIdx">
            <div class="row" v-if="colIdx + rowIdx * 3 < formulas.length">
              <div class="formula" style="background-color: white; padding: 5px; margin-bottom: 20px">
              <a class="" :href="formulas[rowIdx * 3 + colIdx].slug">
                <VueMathjax :formula="formulas[rowIdx * 3 + colIdx].formula"></VueMathjax>
              </a>
            </div>
            </div>

        </div>
      </div>
    </div>
   </div>
</div>
</div>

</template>


<style scoped>
@import '../../assets/css/sciences.css';
</style>