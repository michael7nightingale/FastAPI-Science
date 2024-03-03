<script>
import {activateUser, registerUser} from "@/services/UserService";

export default {
  name: "LoginView",
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
            console.log(responseData)
            document.getElementById("activation").className = document.getElementById("activation").className.replace("hide", "show");
            document.getElementById("main").className = document.getElementById("main").className.replace("show", "hide");
          })
    },
    emailInput(value) {
      this.email = value;
      this.emailError = "";
    },
    usernameInput(value) {
      this.username = value;
      if (this.username.length >= this.usernameMinLength) this.usernameError = "";
    },
    passwordInput(value) {
      this.password = value;
      if (this.password.length >= this.passwordMinLength) this.passwordError = "";
    },
    codeInput(event, idx) {
      let inputValue = event.target.value;
      let currentInput = document.getElementById(idx);
      let nextInput = idx < 6 ? document.getElementById(idx + 1) : false;
      let previosInput = idx > 0 ? document.getElementById(idx - 1) : false;
      if (inputValue.length > 1) {
        currentInput.value = this.code[idx];
        return;
      }
      if (inputValue.length === 1) {
        this.code[idx] = currentInput.value;
        if (nextInput) nextInput.focus();
        return;
      }
      if (inputValue.length === 0) {
        this.code[idx] = "";
        if (previosInput) previosInput.focus();
      }
    },
    submitActivationCode() {
      if (this.code.length !== 6) {
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
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-10 w-auto" :src="'/images/logo.png'"
           alt="Логотип">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
        Регистрация
      </h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium leading-6 text-gray-900 flex">Почта</label>
          <div class="mt-2">
            <input id="email" :name="email" type="email" autocomplete="email" required @input="emailInput($event.target.value)"
                   class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>
        <div>
          <label for="email" class="block text-sm font-medium leading-6 text-gray-900 flex">Логин</label>
          <div class="mt-2">
            <input id="email" :name="username" type="text" autocomplete="text" required @input="usernameInput($event.target.value)"
                   class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>
        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Пароль</label>
            <div class="text-sm">
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Забыли пароль?</a>
            </div>
          </div>
          <div class="mt-2">
            <input id="password" :name="password" type="password" autocomplete="current-password" required @input="passwordInput($event.target.value)"
                   class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <button @click="registerClick" type="button"
                  class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
            Зарегистрироваться
          </button>
        </div>
      </form>
      <p class="mt-10 text-center text-sm text-gray-500">
        Уже есть аккаунт?
        <router-link :to="{name: 'login'}" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
          Войти
        </router-link>
      </p>
    </div>
  </div>
  <div class="container hide" id="activation">
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