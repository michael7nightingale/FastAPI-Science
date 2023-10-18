<script>
import {getScienceDetail} from "/src/services/ScienceService";

export default {
  name: "SciencesDetailView",
  data(){
    return {
      science: {},
      categories: [],
    }
  },
  mounted() {
    console.log(this.$route.params.slug);
    let promise = getScienceDetail(this.$route.params.slug)
    promise.then(response => {
      this.science = response.science;
      this.categories = response.categories;
    })
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
        <div id="faq">
    <ul>
      <li>
        <input type="checkbox" checked>
        <h1 align="center">{{ science.title }}</h1>
      <p class="lead">{{ science.content }}</p>
      </li>
    </ul>
    </div>
    <router-link to="/sciences" class="btn btn-primary btn-large">назад к наукам &raquo;</router-link>
</div>

 <div class="container">
   <div class="category-col row" v-for="category in categories" v-bind:key="category">
         <div class="col-3" style="background-color: #cccccc; margin: 20px">
             <div class="row">
                <img v-if="category.image_path" src="" width="130">
             </div>
         </div>
         <div class="col" style="background-color: #cccccc; margin: 20px">
             <div class="row">
                 <h4 align="center">
                 <router-link v-if="category.is_special" :to="`/special-category/${category.slug}`">{{ category.title  }}</router-link>
                 <router-link v-else :to="{name: 'category', params: {slug: category.slug}}">{{ category.title  }}</router-link>
                 </h4>
             </div>

             <div class="row">
                 <p>{{ category.content.slice(0, 100) }}</p>
             </div>
         </div>

         </div>
   </div>
 </div>
</template>



<style scoped>
@import '../../assets/css/sciences.css';
</style>