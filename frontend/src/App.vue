<script>
import Footer from "@/components/Footer.vue";
import {getUser, logoutUser} from "@/services/Auth";

export default {
  name: "AppItem",
  components: {
    Footer,

  },

  data(){
    return {
      publicPath: process.env.BASE_URL,
      editMeUrl: 'https://github.com/michael7nightingale/FastAPI-Science',

    }
  },

  computed: {
    user(){
      return getUser();
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
       <img :src="`/images/logo.png`" alt="Logo" class="nav-logo" style="width: 120px">
        </router-link>
    <h5 class="my-0 mr-md-auto font-weight-normal">сайт для вычислений</h5>

        <nav class="my-2 my-md-0 mr-md-4">
            <div v-if="user">
              <router-link class="p-2 text-dark" to="/">Главная</router-link>
              <a href="/" @click="githubOpen">
                GitHub
                <img alt="" :src="`/images/github.png`" class="nav-logo" style="width:70px">
              </a>
               <a class="p-2 text-dark" href="" @click="logoutClick">Выйти</a>
               <router-link class="p-2 text-dark" to="/cabinet">Кабинет</router-link>
            </div>
            <div v-else>
              <router-link class="p-2 text-dark" to="/">Главная</router-link>
              <a href="/" @click="githubOpen">
                GitHub
                <img alt="" :src="`/images/github.png`" class="nav-logo" style="width:70px">
              </a>
              <router-link class="p-2 text-dark" to="/auth/login">Вход</router-link>
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
