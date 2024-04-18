<script>

import {activateUser} from "@/services/UserService";

export default {
  name: "ActivationView",
  data() {
    return {
      code: ["", "", "", "", "", ""],
      allowSubmit: false,
      errorText: ""
    }
  },
  methods: {
    codeInput(event) {
      const el = event.target;
      const value = el.value;
      if (value.length > 1) {
        el.value = value[0];
      }
      this.code[el.id.slice(7) - 1] = value.toString();
      this.allowSubmit = !this.code.includes("");
    },
    codeSubmit() {
      activateUser(this.code.join(""))
          .then((response) => {
            if (response.status === 200) {
              this.$router.push({name: "login"})
            } else {
              this.errorText = "Неверный код"
            }
          })
          .catch(() => {
            this.errorText = "Неверный код"
          })
    }
  }

}
</script>


<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-10 w-auto" :src="'/images/logo.png'"
           alt="Логотип">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
        Активация аккаунта
      </h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6">
        <div class="flex">
          <label class="mx-auto text-center text-gray-900">
            На указанную почту мы выслали код для активации аккаунта
          </label>
        </div>
        <div>
          <div class="mt-2 flex gap-x-1.5">
            <input id="number-1" type="number" maxlength="1" required
                   @input="codeInput($event)"
                   class="code-input block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            <input id="number-2" type="number" maxlength="1" required
                   @input="codeInput($event)"
                   class="code-input block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            <input id="number-3" type="number" maxlength="1" required
                   @input="codeInput($event)"
                   class="code-input block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            <input id="number-4" type="number" maxlength="1" required
                   @input="codeInput($event)"
                   class="code-input block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            <input id="number-5" type="number" maxlength="1" required
                   @input="codeInput($event)"
                   class="code-input block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            <input id="number-6" type="number" maxlength="1" required
                   @input="codeInput($event)"
                   class="code-input block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>
        <div>
          <button type="button" :disabled="!allowSubmit" @click="codeSubmit"
                  :class="`flex w-full justify-center rounded-md ${allowSubmit ? 'bg-indigo-600': 'bg-indigo-200'} px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm ${allowSubmit ? 'bg-indigo-500 ': ''} focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600`">
            Активировать
          </button>
        </div>
      </form>
      <p class="mt-10 text-center text-sm text-gray-500">
        <router-link :to="{name: 'login'}" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
          Войти
        </router-link>
        или
        <router-link :to="{name: 'register'}" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
          Зарегистрироваться
        </router-link>
      </p>
    </div>
  </div>
</template>


<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}

.code-input {
  -moz-appearance: textfield;
  text-align: center;
}
</style>