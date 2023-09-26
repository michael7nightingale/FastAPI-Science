<script>
import {loginUser} from "@/services/UserService";
import {setUser} from "@/services/Auth";
import OAuth from "@/components/OAuth.vue";

export default {
  name: "LoginView",
  components: {OAuth},
  data(){
    return{
      username: null,
      password: null,
    }
  },
  methods: {
    loginClick(){
        let data;
        loginUser(this.username, this.password)
            .then((response) => {
              data = response.data;
              setUser(data.access_token);
              window.location = this.$router.resolve({name: "homepage"}).fullPath;
            })
            .catch((error) => {
              alert(error.response.data.detail);
            })
    },

    usernameInput(value){
      this.username = value;
    },
    passwordInput(value){
      this.password = value;
    }
  }

}

</script>

<template>
<div class="container login-container">
  <h3 align="center">Log in</h3>
    <div class="form-item">
      <input type="text" placeholder="Username" :value="username" @input="usernameInput($event.target.value)" class="form-style" autocomplete="off"/>
    </div>
    <div class="form-item">
      <input type="password" placeholder="Password" :value="password" @input="passwordInput($event.target.value)" id="password" class="form-style" />
    </div>
    <div class="form-item">
        <router-link to="/auth/register" class="pull-left"><small>registration</small></router-link>
        <router-link to="/auth/register" class="pull-left margin-pull-left"><small>forgot password?</small></router-link>
        <button class="btn login pull-right" @click="loginClick" style="background-color: #fff; border:1px solid #55b1df; color:#55b1df; cursor:pointer;">
        Log In
      </button>
        <div class="clear-fix"></div>
    </div>
    <OAuth/>
</div>
</template>

<style>
@import '../../assets/css/login.css';
</style>