<script>
import {registerUser} from "@/services/UserService";
import OAuth from "@/components/OAuth.vue";

export default {
  name: "LoginView",
  components: {OAuth},
  data() {
    return {
      username: null,
      password: null,
      email: null
    }
  },
  methods: {
    registerClick() {
      let data;
      registerUser(this.email, this.username, this.password)
          .then(responseData => {
            data = responseData.data;
            console.log(data);
            this.$router.push("/auth/login")
          })
          .catch((error) => {
            alert(error.response.data.detail);
          });
    },
    emailInput(value) {
      this.email = value;
    },
    usernameInput(value) {
      this.username = value;
    },
    passwordInput(value) {
      this.password = value;
    }
  }
}

</script>

<template>
<div class="container login-container">
    <h3 align="center">Registration</h3>
    <div class="form-item">
      <input type="email" :value="email" @input="emailInput($event.target.value)" placeholder="Email" id="email" class="form-style" autocomplete="off"/>
    </div>
    <div class="form-item">
      <input type="text" placeholder="Username" :value="username" @input="usernameInput($event.target.value)" class="form-style" autocomplete="off"/>
    </div>
    <div class="form-item">
      <input type="password" placeholder="Password" :value="password" @input="passwordInput($event.target.value)" id="password" class="form-style" />
    </div>
    <div class="form-item">
        <router-link to="/auth/login" class="pull-left"><small>log in</small></router-link>
        <button class="btn login pull-right" @click="registerClick" style="background-color: #fff; border:1px solid #55b1df; color:#55b1df; cursor:pointer;">
          Register
        </button>
        <div class="clear-fix"></div>
    </div>
    <OAuth/>
</div>
</template>

<style>
@import '../../assets/css/login.css';
</style>