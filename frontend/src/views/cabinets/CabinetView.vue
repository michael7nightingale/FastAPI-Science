<script>

import {getHistoryList} from "@/services/CabinetService";

export default {
  name: "CabinetView",
  methods: {
    parseDatetime(dateString) {
      let dateTime = new Date(Date.parse(dateString));
      return `${dateTime.toLocaleDateString()} ${dateTime.toLocaleTimeString()}`
    }
  },
  data() {
    return {
      history: "history",

    }
  },
  computed: {
    User() {
      return JSON.parse(localStorage.userData);
    },
    UserRegisteredDate() {
      let dateTime = new Date(Date.parse(this.User.time_registered));
      return dateTime.toLocaleDateString()
    }
  },
  mounted() {
    getHistoryList()
        .then((response) => {
          this.history = response.data;
        })
  }
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
          <span class="text-gray-800">Личный Кабинет</span>
        </li>
      </ol>
    </nav>
    <div class="lg:flex lg:items-center lg:justify-between">
      <div class="min-w-0 flex-1">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
          {{ User.username }}
        </h2>
        <div class="mt-1 flex flex-col sm:mt-0 sm:flex-row sm:flex-wrap sm:space-x-6">
          <div class="mt-2 flex items-center text-sm text-gray-500">
            Почта: {{ User.email }}
          </div>
          <div class="mt-2 flex items-center text-sm text-gray-500">
            <svg class="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" viewBox="0 0 20 20" fill="currentColor"
                 aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M5.75 2a.75.75 0 01.75.75V4h7V2.75a.75.75 0 011.5 0V4h.25A2.75 2.75 0 0118 6.75v8.5A2.75 2.75 0 0115.25 18H4.75A2.75 2.75 0 012 15.25v-8.5A2.75 2.75 0 014.75 4H5V2.75A.75.75 0 015.75 2zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75z"
                    clip-rule="evenodd"/>
            </svg>
            Зарегистрирован {{ UserRegisteredDate }}
          </div>
        </div>
      </div>
<!--      <div class="mt-5 flex lg:ml-4 lg:mt-0">-->
<!--    <span class="hidden sm:block">-->
<!--      <button type="button"-->
<!--              class="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">-->
<!--        <svg class="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">-->
<!--          <path-->
<!--              d="M2.695 14.763l-1.262 3.154a.5.5 0 00.65.65l3.155-1.262a4 4 0 001.343-.885L17.5 5.5a2.121 2.121 0 00-3-3L3.58 13.42a4 4 0 00-.885 1.343z"/>-->
<!--        </svg>-->
<!--        Edit-->
<!--      </button>-->
<!--    </span>-->

<!--        <span class="ml-3 hidden sm:block">-->
<!--      <button type="button"-->
<!--              class="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">-->
<!--        <svg class="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">-->
<!--          <path-->
<!--              d="M12.232 4.232a2.5 2.5 0 013.536 3.536l-1.225 1.224a.75.75 0 001.061 1.06l1.224-1.224a4 4 0 00-5.656-5.656l-3 3a4 4 0 00.225 5.865.75.75 0 00.977-1.138 2.5 2.5 0 01-.142-3.667l3-3z"/>-->
<!--          <path-->
<!--              d="M11.603 7.963a.75.75 0 00-.977 1.138 2.5 2.5 0 01.142 3.667l-3 3a2.5 2.5 0 01-3.536-3.536l1.225-1.224a.75.75 0 00-1.061-1.06l-1.224 1.224a4 4 0 105.656 5.656l3-3a4 4 0 00-.225-5.865z"/>-->
<!--        </svg>-->
<!--        View-->
<!--      </button>-->
<!--    </span>-->
<!--        <span class="sm:ml-3">-->
<!--      <button type="button"-->
<!--              class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">-->
<!--        <svg class="-ml-0.5 mr-1.5 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">-->
<!--          <path fill-rule="evenodd"-->
<!--                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"-->
<!--                clip-rule="evenodd"/>-->
<!--        </svg>-->
<!--        Publish-->
<!--      </button>-->
<!--    </span>-->
<!--        &lt;!&ndash; Dropdown &ndash;&gt;-->
<!--        <div class="relative ml-3 sm:hidden">-->
<!--          <button type="button"-->
<!--                  class="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400"-->
<!--                  id="mobile-menu-button" aria-expanded="false" aria-haspopup="true">-->
<!--            More-->
<!--            <svg class="-mr-1 ml-1.5 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">-->
<!--              <path fill-rule="evenodd"-->
<!--                    d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"-->
<!--                    clip-rule="evenodd"/>-->
<!--            </svg>-->
<!--          </button>-->

<!--          &lt;!&ndash;-->
<!--            Dropdown menu, show/hide based on menu state.-->

<!--            Entering: "transition ease-out duration-200"-->
<!--              From: "transform opacity-0 scale-95"-->
<!--              To: "transform opacity-100 scale-100"-->
<!--            Leaving: "transition ease-in duration-75"-->
<!--              From: "transform opacity-100 scale-100"-->
<!--              To: "transform opacity-0 scale-95"-->
<!--          &ndash;&gt;-->
<!--          <div-->
<!--              class="absolute right-0 z-10 -mr-1 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"-->
<!--              role="menu" aria-orientation="vertical" aria-labelledby="mobile-menu-button" tabindex="-1">-->
<!--            &lt;!&ndash; Active: "bg-gray-100", Not Active: "" &ndash;&gt;-->
<!--            <a href="#" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1"-->
<!--               id="mobile-menu-item-0">Edit</a>-->
<!--            <a href="#" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1"-->
<!--               id="mobile-menu-item-1">View</a>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
    </div>
    <div class="mt-5 text-center">
      <h3 class="text-xl font-bold leading-8 text-gray-700 sm:truncate sm:text-2xl sm:tracking-tight">История
        вычислений</h3>
    </div>
    <table class="items-center bg-transparent w-full border-collapse mt-5">
      <thead>
      <tr>
        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
          Результат
        </th>
        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
          Формула
        </th>
        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
          Категория
        </th>
        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
          Дата и время
        </th>
      </tr>
      </thead>

      <tbody>
      <tr v-for="result in history" v-bind:key="result.id"
          class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
        <td class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 ">
          {{ result.result }}
        </td>
        <th class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left text-blueGray-700 ">
          <router-link :to="{name: 'formula', params: {slug: result.formula?.slug || 'formula'}}">
            {{ result.formula?.title }}
          </router-link>
        </th>
        <td class="border-t-0 px-6 align-center border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
          <router-link :to="{name: 'category', params: {slug: result.category?.slug || 'category'}}">
            {{ result.category?.title }}
          </router-link>
        </td>
        <td class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
          <i class="fas fa-arrow-up text-emerald-500 mr-4"></i>
          {{ parseDatetime(result.date_time) }}
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style>

</style>