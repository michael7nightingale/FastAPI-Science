<script>
import {loginUser} from "@/services/UserService";
import {setUser} from "@/services/Auth";

export default {
  name: "LoginView",
  data() {
    return {
      errorText: "",
      loginMinLength: 6,
      passwordMinLength: 6,
      login: "",
      loginError: "",
      password: "",
      passwordError: "",

    }
  },
  methods: {
    loginClick() {
      let data;
      loginUser(this.login, this.password)
          .then((response) => {
            data = response.data;
            setUser(data.access_token)
                .then(() => {
                  window.location = this.$router.resolve({name: "homepage"}).fullPath;
                });
          })
          .catch((error) => {
            this.errorText = error.response.data.detail;
          })
    },

    loginInput(value) {
      this.login = value;
      if (this.login.length >= this.loginMinLength) this.loginError = "";
    },
    passwordInput(value) {
      this.password = value;
      if (this.password.length >= this.passwordMinLength) this.passwordError = "";
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
        Вход в аккаунт
      </h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium leading-6 text-gray-900 flex">Логин</label>
          <div class="mt-2">
            <input id="email" :name="login" type="text" autocomplete="text" required @input="loginInput($event.target.value)"
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
            <input id="password" :name="password" type="password" autocomplete="current-password" required  @input="passwordInput($event.target.value)"
                   class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <button @click="loginClick" type="button"
                  class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
            Войти
          </button>
        </div>
      </form>
      <p class="mt-10 text-center text-sm text-gray-500">
        Нет аккаунта?
        <router-link :to="{name: 'register'}" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
          Зарегистрироваться
        </router-link>
      </p>
    </div>
  </div>
</template>

<style>
</style>
