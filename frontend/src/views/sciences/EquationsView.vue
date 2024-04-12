<script>
import {getSpecialCategoryDetail, postEquations} from "@/services/ScienceService";

export default {
  "name": "EquationsView",
  data() {
    return {
      storage: [""],
      science: {slug: '-'},
      category: {slug: '-'},
      result: []
    }
  },

  mounted() {
    let promise = getSpecialCategoryDetail(this.$route.name)
    promise.then(response => {
      this.science = response.science;
      this.category = response.category;
      this.plotPath = response.plotPath
    })

  },

  methods: {

    solveEquations() {
      let data = {
        equations: this.storage
      }
      postEquations(data)
          .then((response) => {
            let message = response.detail;
            if (message) {
              alert(message)
            } else {
              this.result = [];
              for (let variable of Object.keys(response.result)) {
                this.result.push({variable: variable, result: response.result[variable]})
              }
              this.result = response.result
            }
          })
          // .catch((error) => {
          //   if (error.response.status === 401){
          //     alert("Вы не авторизованы")
          //     this.$router.push({name: 'login'})
          //   }
          // })
    },

    inputFunction(value, name) {
      this.storage[name] = value;
    },

    addFunction() {
      let storageProxy = this.storage;
      storageProxy.push("");
      this.storage = storageProxy;
    },

    deleteFunction(idx) {
      if (this.storage.length === 1) return;
      let storageProxy = this.storage;
      storageProxy.splice(idx, 1);
      this.storage = storageProxy;
    },
  },

}
</script>

<template>
  <div class="body-content">
    <nav class="text-sm sm:text-base bg-white p-4 md:p-6 lg:p-6 rounded-md">
      <ol class="list-none p-0 inline-flex space-x-2">
        <li class="flex items-center">
          <router-link :to="{name: 'homepage'}">
            <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512"
                 class="cursor-pointer hover:fill-blue-500 transition-colors duration-300" fill="#4b5563">
              <path
                  d="M575.8 255.5c0 18-15 32.1-32 32.1h-32l.7 160.2c0 2.7-.2 5.4-.5 8.1V472c0 22.1-17.9 40-40 40H456c-1.1 0-2.2 0-3.3-.1c-1.4 .1-2.8 .1-4.2 .1H416 392c-22.1 0-40-17.9-40-40V448 384c0-17.7-14.3-32-32-32H256c-17.7 0-32 14.3-32 32v64 24c0 22.1-17.9 40-40 40H160 128.1c-1.5 0-3-.1-4.5-.2c-1.2 .1-2.4 .2-3.6 .2H104c-22.1 0-40-17.9-40-40V360c0-.9 0-1.9 .1-2.8V287.6H32c-18 0-32-14-32-32.1c0-9 3-17 10-24L266.4 8c7-7 15-8 22-8s15 2 21 7L564.8 231.5c8 7 12 15 11 24z"/>
            </svg>
          </router-link>
          <span class="mx-2">/</span>
        </li>
        <li class="flex items-center">
          <router-link :to="{name: 'science', params: {slug: science.slug}}">
            {{ science.title }}
          </router-link>
          <span class="mx-2">/</span>
        </li>
        <li class="flex items-center">
          <span class="text-gray-800">{{ category.title }}</span>
        </li>
      </ol>
    </nav>
    <div class="flex gap-3">
      <button
            class="flex-none btn overflow-hidden relative w-14 bg-blue-500 text-white py-1 px-1 rounded-xl font-bold uppercase -- before:block before:absolute before:h-full before:w-1/2 before:rounded-full before:bg-orange-400 before:top-0 before:left-1/4 before:transition-transform before:opacity-0 before:hover:opacity-100 hover:text-orange-200 hover:before:animate-ping transition-all duration-300"
        @click="addFunction"
      >
          <svg xmlns="http://www.w3.org/2000/svg" width="46" height="46" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
  <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
</svg>
        </button>
      <h1 class="flex-initial m-auto text-2xl font-semibold leading-7 text-gray-900 text-center">Решение уравнений</h1>
    </div>
    <div class="border-b border-gray-900/25 py-5">
      <fieldset class="pb-3" v-for="n in Array(storage.length).keys()" :key="n">
        <div class="grid">
          <div class="">
            <label class="block">
                  <span class="font-semibold leading-6 text-gray-900 text-center">
                    Уравнение №{{ n+1 }}
                  </span>
            </label>
            <div class="mt-2 flex gap-4">
              <input type="text"
                     :value="storage[n]"
                     @input="inputFunction($event.target.value, n)"
                     placeholder="Введите уравнение..."
                     class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
              <button
                class="m-auto btn overflow-hidden relative w-64 bg-red-500 text-white py-3 px-3 rounded-xl font-semibold uppercase -- before:block before:absolute before:h-full before:w-1/2 before:rounded-full before:bg-orange-400 before:top-0 before:left-1/4 before:transition-transform before:opacity-0 before:hover:opacity-100 hover:text-orange-200 hover:before:animate-ping transition-all duration-300"
                @click="deleteFunction(n)">
              <span class="relative">Удалить</span>
            </button>
            </div>
          </div>
        </div>
      </fieldset>
    </div>

    <div class="flex " style="margin: 20px">
      <div class="w-64">
        <button class="border-2 py-3 px-3 rounded-xl w-40" @click="solveEquations">Решить</button>
      </div>
      <div class="py-3 px-3 text-center">
          <ul class="list-disc">
            <li v-for="(value, key) in result" v-bind:key="key">
              <h4 class="text-2xl">{{key}} = {{value}}</h4>
            </li>
          </ul>
      </div>
    </div>



  </div>
</template>

<style scoped>

</style>