<script>
import {registerUser} from "@/services/UserService";
import OAuth from "@/components/OAuth.vue";

export default {
  name: "LoginView",
  components: {OAuth},
  data() {
    return {
      usernameMinLength: 6,
      passwordMinLength: 6,
      emailMinLength: 6,
      username: "",
      usernameError: "",
      password: "",
      passwordError: "",
      email: "",
      emailError: "",

    }
  },
  methods: {
    registerClick() {
      let data;
      let wereError = false;
      if (this.username.length < this.usernameMinLength) {
        wereError = true;
        this.usernameError = `Имя пользователя должно содержать от ${this.usernameMinLength} символов`
      }
      if (this.password.length < this.passwordMinLength) {
        wereError = true;
        this.passwordError = `Пароль должно содержать от ${this.passwordMinLength} символов`
      }
      if (!this.email.match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
        wereError = true;
        this.emailError = `Неверный адрес электронной почты`
      }
      if (wereError) return;
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
      this.emailError = "";
    },
    usernameInput(value){
      this.username = value;
      if (this.username.length >= this.usernameMinLength) this.usernameError = "";
    },
    passwordInput(value){
      this.password = value;
      if (this.password.length >= this.passwordMinLength) this.passwordError = "";
    }
  }
}

</script>

<template>
<div class="container login-container">
    <h3 align="center">Регистрация</h3>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Почта</label>
      <input type="email" :value="email" @input="emailInput($event.target.value)" placeholder="Почта:" id="email" class="form-style" autocomplete="off"/>
      <p class="text-danger" style="margin: 10px">{{ emailError }}</p>
    </div>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Имя пользователя</label>
      <input type="text" placeholder="Имя пользователя:" :value="username" @input="usernameInput($event.target.value)" class="form-style" autocomplete="off"/>
      <p class="text-danger" style="margin: 10px">{{ usernameError }}</p>
    </div>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Пароль</label>
      <input type="password" placeholder="Пароль:" :value="password" @input="passwordInput($event.target.value)" id="password" class="form-style" />
      <p class="text-danger" style="margin: 10px">{{ passwordError }}</p>
    </div>
    <div class="form-item">
        <router-link to="/auth/login" class="pull-left"><small>Вход</small></router-link>
        <button class="btn login pull-right" @click="registerClick" style="background-color: #fff; border:1px solid #55b1df; color:#55b1df; cursor:pointer;">
          Зарегистрироваться
        </button>
        <div class="clear-fix"></div>
    </div>
    <OAuth/>
</div>
</template>

<style>
@import '../../assets/css/login.css';
</style>