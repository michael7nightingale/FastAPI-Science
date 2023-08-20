<script>
import Footer from "@/components/Footer.vue";
import {logoutUser} from "@/services/Auth";

export default {
  name: "AppItem",
  components: {
    Footer,

  },

  data(){
    return {
      publicPath: process.env.BASE_URL,
      editMeUrl: 'https://github.com/michael7nightingale/FastAPI-Science',
      logoUrl: "http://127.0.0.1:8001/static/main/images/logo.png",

    }
  },

  computed: {
    user(){
      return Boolean(localStorage.user);
    }
  },

  methods: {
    logoutClick(){
      logoutUser()
    },
    githubOpen(){
      window.open(this.editMeUrl, "_blank");
    }
  },

}
</script>


<template>
    <div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm">
      <router-link to="/">
       <img :src="logoUrl" alt="Logo" class="nav-logo" style="width: 120px">
        </router-link>
    <h5 class="my-0 mr-md-auto font-weight-normal">сайт для вычислений</h5>



        <nav class="my-2 my-md-0 mr-md-4">
            <div v-if="user">
              <a href="/" @click="githubOpen">
                Edit me
                <img alt="" :src="`images/github.png`" class="nav-logo" style="width:70px">
              </a>
              <router-link class="p-2 text-dark" to="/">Home</router-link>
               <a class="p-2 text-dark" href="" @click="logoutClick">Logout</a>
               <router-link class="p-2 text-dark" to="/cabinet">Cabinet</router-link>
            </div>
            <div v-else>
              <a href="/" @click="githubOpen">
                Edit me
                <img alt="" :src="`images/github.png`" class="nav-logo" style="width:70px">
              </a>
              <router-link class="p-2 text-dark" to="/">Home</router-link>
              <router-link class="p-2 text-dark" to="/auth/login">Login</router-link>
            </div>
        </nav>
    </div>

  <div class="body-content background">
    <hr/>
    <router-view/>
  </div>

  <Footer/>
</template>

<style>
@import './assets/css/global.css';
</style>
