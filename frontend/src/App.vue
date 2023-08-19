<template>
    <div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm">
    <h5 class="my-0 mr-md-auto font-weight-normal">сайт для вычислений</h5>
        <router-link to="/">
          <img :src="`${publicPath}images/logo.png`" class="nav-logo" width="17%" height="10%">
        </router-link>

        <nav class="my-2 my-md-0 mr-md-4">
            <a href="{{ editMeUrl }}">
                Edit me
                <img alt="" :src="`${publicPath}images/github.png`" class="nav-logo" width=10% height="10%">
            </a>

            <router-link class="p-2 text-dark" to="/">Home</router-link>
           <router-link class="p-2 text-dark" to="/auth/login">Login</router-link>
        </nav>
    </div>

  <div class="body-content background"  >
    <hr/>
    <router-view/>
  </div>

  <Footer/>
</template>

<style>
.background{
        //background-image: url("");
        min-height: 700px;
}
.white_text{
  color: whitesmoke;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

<script>
import Footer from "@/components/Footer.vue";

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
  }
}
</script>