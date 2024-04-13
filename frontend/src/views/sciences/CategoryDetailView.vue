<template>
  <div class="body-content">
    <!--    <ul role="list" class="divide-y divide-gray-100">-->
    <!--      <li class="flex justify-between gap-x-6 py-5" v-for="formula in categoryData.formulas" v-bind:key="formula.id">-->
    <!--        <router-link :to="{name: 'formula', params: {slug: formula.slug}}" class="flex min-w-0 gap-x-4">-->
    <!--          <img class="h-12 w-12 flex-none rounded-full bg-gray-50"-->
    <!--               src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"-->
    <!--               alt="">-->
    <!--          <div class="min-w-0 flex-auto">-->
    <!--            <p class="text-sm font-semibold leading-6 text-gray-900">{{ formula.title }}</p>-->
    <!--          </div>-->
    <!--        </router-link>-->
    <!--        <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">-->
    <!--          <p class="text-sm leading-6 text-gray-900">{{formula.formula}}</p>-->
    <!--          <div>-->
    <!--            &lt;!&ndash;          <vue-mathjax formula="$$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.$$"></vue-mathjax>&ndash;&gt;-->
    <!--          </div>-->
    <!--          &lt;!&ndash;          <div class="demo-container">&ndash;&gt;-->
    <!--          &lt;!&ndash;              <textarea v-model="formula_" cols="30" rows="10"></textarea>&ndash;&gt;-->
    <!--          &lt;!&ndash;              <vue-mathjax :key="formula_" :formula="formula_"></vue-mathjax>&ndash;&gt;-->
    <!--          &lt;!&ndash;          </div>&ndash;&gt;-->
    <!--          <p class="mt-1 text-xs leading-5 text-gray-500">Last seen-->
    <!--            <time datetime="2023-01-23T13:23Z">3h ago</time>-->
    <!--          </p>-->
    <!--        </div>-->
    <!--      </li>-->
    <!--    </ul>-->
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
          <span class="text-gray-800">{{ categoryData.title }}</span>
        </li>
      </ol>
    </nav>
    <div class="grid grid-cols-1 gap-4 mt-3 sm:grid-cols-3 lg:mt-20">
      <div class="lg:w-1/3 border-black" v-for="formula in categoryData.formulas" v-bind:key="formula.id">
        <router-link :to="{name: 'formula', params: {slug: formula.slug}}" class="flex min-w-0 gap-x-4">
          <!--          <img class="h-20 w-20 flex-none rounded-full bg-gray-50"-->
          <!--               :src="buildStaticUrl(`sciences/${category.image_path}`)"-->
          <!--               :alt="category.title">-->
          <div class="flex-auto">
            <p class="text-sm font-semibold leading-6 text-gray-900">{{ formula.title }}</p>
            <p class="mt-1 truncate text-xs leading-5 text-gray-500">{{ formula.formula }}</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>


<script>
import {getCategoryDetail} from "/src/services/ScienceService";


export default {
  name: "CategoryDetailView",
  data() {
    return {
      scienceData: {slug: 'ps'},
      formulas: null,
      formula_: '$$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.$$',
      categoryData: {},
    }
  },
  mounted() {
    let promise = getCategoryDetail(this.$route.params.slug)
    promise.then(response => {
      this.categoryData = response;
      this.scienceData = response.science;
    })
        .catch((error) => {
          switch (error.response.status) {
            case 404:
              if (error.response.data.science && error.response.data.category) {
                this.scienceData = error.response.data.science;
                this.categoryData = error.response.data.category;
              }
          }
        })
  },

}
</script>

<style scoped>
@import "../../../node_modules/katex/dist/katex.min.css";
@import '../../assets/css/sciences.css';
</style>