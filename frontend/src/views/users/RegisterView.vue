<script>
import {activateUser, registerUser} from "@/services/UserService";
import OAuth from "@/components/OAuth.vue";

export default {
  name: "LoginView",
  components: {OAuth},
  data() {
    return {
      errorText: "",
      codeErrorText: "",
      usernameMinLength: 6,
      passwordMinLength: 6,
      emailMinLength: 6,
      username: "",
      usernameError: "",
      password: "",
      passwordError: "",
      email: "",
      emailError: "",
      code: ["", "", "", "", "", ""],

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
          .then((responseData) => {
            data = responseData.data;
            console.log(data);
            document.getElementById("activation").className = document.getElementById("activation").className.replace("hide", "show");
             document.getElementById("main").className = document.getElementById("main").className.replace("show", "hide");
          })
          .catch((error) => {
            this.errorText = error.response.data.detail;
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
    },
    codeInput(event, idx){
      let inputValue = event.target.value;
      let currentInput = document.getElementById(idx);
      let nextInput = idx < 6 ? document.getElementById(idx + 1) : false;
      let previosInput = idx > 0 ? document.getElementById(idx - 1) : false;
      if (inputValue.length > 1){
        currentInput.value = this.code[idx]; return;
      }
      if (inputValue.length === 1){
        this.code[idx] = currentInput.value;
        if (nextInput) nextInput.focus(); return;
      }
      if (inputValue.length === 0){
        this.code[idx] = "";
        if (previosInput) previosInput.focus();
      }
    },
    submitActivationCode(){
      if (this.code.length !== 6){
        this.codeErrorText = "Длина кода должна быть равна 6 цифрам"
        return;
      }
      activateUser(this.code.join(""))
          .then((response) => {
            response;
            this.$router.push({name: "login"})
          })
          .catch((error) => {
            this.codeErrorText = error.response.data.detail;
          })
    },
  }
}

</script>

<template>
<div class="container login-container show" id="main">
    <h3 align="center">Регистрация</h3>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Почта</label>
      <input type="email" :value="email" @input="emailInput($event.target.value)" placeholder="Почта:" id="email" class="form-style" autocomplete="off"/>
      <p class="text-danger text-margin">{{ emailError }}</p>
    </div>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Имя пользователя</label>
      <input type="text" placeholder="Имя пользователя:" :value="username" @input="usernameInput($event.target.value)" class="form-style" autocomplete="off"/>
      <p class="text-danger text-margin">{{ usernameError }}</p>
    </div>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Пароль</label>
      <input type="password" placeholder="Пароль:" :value="password" @input="passwordInput($event.target.value)" id="password" class="form-style" />
      <p class="text-danger text-margin">{{ passwordError }}</p>
    </div>
   <p class="text-danger text-margin">{{ errorText }}</p>
    <div class="form-item">
        <router-link to="/auth/login" class="pull-left"><small>Вход</small></router-link>
        <button class="btn login pull-right" @click="registerClick" style="background-color: #fff; border:1px solid #55b1df; color:#55b1df; cursor:pointer;">
          Зарегистрироваться
        </button>
        <div class="clear-fix"></div>
    </div>
    <OAuth/>
</div>
  <div class="container" id="activation">
  <h3 align="center">Подтверждение почты</h3>
    <label class="text-margin">Мы отправили код для подтверждения вам на почту</label>
       <div class="input-field">
         <input
             :id="data"
             v-for="(idx, data) in Array(6)" :key="data"
             type="number"
             @input="codeInput($event, data)"
         />
       </div>
      <p class="text-danger text-margin">{{ codeErrorText }}</p>
       <button class="activation-btn" type="button" @click="submitActivationCode">Подтвердить</button>
</div>
</template>

<style>
@import '../../assets/css/login.css';
@import "../../assets/css/activation.css";
</style>