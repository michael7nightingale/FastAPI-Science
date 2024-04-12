<script>
import {countResult, getFormulaDetail} from "/src/services/ScienceService";

export default {
  name: "CategoryDetailView",
  data() {
    return {
      formulaData: {},
      scienceData: {},
      categoryData: {},
      info: {},
      result: "?",
      findMark: null,
      numsComma: [10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      storage: {numsComma: 10}
    }
  },
  mounted() {
    let promise = getFormulaDetail(this.$route.params.slug)
    promise.then(response => {
      this.formulaData = response;
      this.scienceData = response.science;
      this.categoryData = response.category;
      let info = JSON.parse(JSON.stringify(response.info));
      this.info = info;
      this.findMark = Object.keys(info.literals)[0];
    })
  },
  methods: {
    tabClick(event, literal) {
      const tabcontents = document.getElementsByClassName("tabcontent");
      for (let tabcontent of tabcontents) {
        if (tabcontent.id !== `${literal}-tab-content`) {
          tabcontent.classList.add("hidden")
        } else {
          tabcontent.classList.remove("hidden")
        }
      }
      this.findMark = literal;
      document.querySelectorAll(".tablink").forEach((el) => el.classList.remove("bg-blue-200"))
      event.target.classList.add("bg-blue-200");
    },

    numberInput(event, literal) {
      this.storage[literal] = event.target.value;
    },

    numsCommaSelect(event) {
      this.storage.numsComma = event.target.value;
    },

    siSelect(event, literal) {
      this.storage[literal + 'si'] = event.target.value;
    },

    getLiteralsExceptFindMark() {
      let literals = [];
      for (const literal of Object.keys(this.info.literals)) {
        if (literal !== this.findMark) {
          literals.push(literal);
        }
      }
      return literals;
    },

    checkStorage() {
      let neededLiterals = this.getLiteralsExceptFindMark();
      let isCorrectData = true;
      let errorMessage = ""
      for (const literal of neededLiterals) {
        if (!(this.storage[literal] && this.storage[`${literal}si`])) {
          isCorrectData = false;
          errorMessage = "Заполните все поля"
        }
      }
        if (errorMessage) alert(errorMessage);
      return isCorrectData;
    },

    countResult() {
      let result;
      let count = this.checkStorage();
      if (count) {
        countResult(this.$route.params.slug, this.storage, this.storage .numsComma, this.findMark)
            .then(responseData => {
              result = responseData.result;
              this.result = result;
            })
            .catch((error) => {
              switch (error.response.status) {
                case 401: {
                  alert("Авторизуйтесь, чтобы воспользоваться функцией вычисления");
                  this.$router.push({name: "login", query: {redirect: this.$route.path}});
                  break;
                }
                case 400: {
                  alert(error.response.data.detail)
                }
              }
            })
      }

    }

  }

}
</script>

<template>
  <!-- eslint-disable vue/no-use-v-if-with-v-for,vue/no-confusing-v-for-v-if -->
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
          <router-link :to="{name: 'science', params: {slug: scienceData.slug}}">{{ scienceData.title }}</router-link>
          <span class="mx-2">/</span>
        </li>
        <li class="flex items-center">
          <router-link :to="{name: 'category', params: {slug: categoryData.slug}}">{{ categoryData.title }}</router-link>
          <span class="mx-2">/</span>
        </li>
        <li class="flex items-center">
          <span class="text-gray-800">{{ formulaData.title }}</span>
        </li>
      </ol>
    </nav>
    <div class="space-y-5">
      <div class="tabs">
        <ul class="-mb-px flex items-center text-sm font-medium">
          <li class="flex-1" v-for="literal in this.info.literals" v-bind:key="literal"
              @click="tabClick($event, literal.literal)">
            <a v-if="!(literal.is_constant)"
               :class="`tablink hover:bg-blue-600/20 font-semibold relative border-2 border-solid border-current flex items-center justify-center gap-2 px-1 py-3 text-blue-700 after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-full after:bg-blue-700 hover:text-blue-700 ${literal.literal === findMark ? 'bg-blue-200': ''}`"
            >
              Найти {{ literal.literal }}
            </a>
          </li>
        </ul>
      </div>
      <div class="border-b border-gray-900/25 pb-12">
        <h2 class="text-base font-semibold leading-7 text-gray-900">Информация для вычислений</h2>
        <p class="mt-1 text-sm leading-6 text-gray-600">Укажите общие параметры для выходных данных</p>
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <label for="nums_comma">Цифр после запятой: </label>
          <select title="nums_comma" name="nums_comma" id="nums_comma" @change="numsCommaSelect($event)"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
            <option
                v-for="n in numsComma"
                :value="n"
                v-bind:key="n"
            >
              {{ n }}
            </option>
          </select>
          <h3 class="text-base text-center leading-6 font-semibold text-gray-900">{{ ` = ${result}` }}</h3>
        </div>
      </div>
      <div class="tabs-content">
        <h2 class="text-base font-semibold leading-7 text-gray-900 text-center">Значения переменных</h2>
        <div v-for="literal_ in this.info.literals" v-bind:key="literal_"
             :id="`${literal_.literal}-tab-content`"
             :class="`tabcontent ${literal_.literal === findMark ? '' : 'hidden'}`">
          <fieldset v-for="literal in this.info.literals" v-bind:key="literal">
            <div v-if="literal.literal !== findMark"
                 class="border-b border-gray-900/10 py-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div class="sm:col-span-3">
                <label :for="`${literal.literal}si`" class="block text-sm font-medium leading-6 text-gray-900">
                  Единицы измерения
                </label>
                <div class="mt-2">
                  <select :name="`${literal.literal}si`"
                          :id="`${literal.literal}si`"
                          @change="siSelect($event, literal.literal)"
                          class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
                    <option
                        v-for="(ed, name) in literal.si"
                        v-bind:key="ed"
                        :value="name"
                        :selected="ed === '1' ? '' : 'selected'"
                    >
                      {{ ed === 1 ? storage[`${literal.literal}si`] = name : name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="">
                <label :for="literal.literal" class="block">
                  <span class="font-semibold leading-6 text-gray-900 text-center">
                    {{ literal.literal }} =
                  </span>
                </label>
                <div class="mt-2">
                  <input type="text" :id="literal.literal"
                         @input="numberInput($event, literal.literal)"
                         :value="storage[literal.literal]"
                         class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                </div>
              </div>
            </div>
          </fieldset>
        </div>

      </div>
      <div class="flex">
        <button
            class="m-auto btn overflow-hidden relative w-64 bg-blue-500 text-white py-4 px-4 rounded-xl font-bold uppercase -- before:block before:absolute before:h-full before:w-1/2 before:rounded-full before:bg-orange-400 before:top-0 before:left-1/4 before:transition-transform before:opacity-0 before:hover:opacity-100 hover:text-orange-200 hover:before:animate-ping transition-all duration-300"
            @click="countResult">
          <span class="relative">Считать</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../../assets/css/sciences.css';
</style>
