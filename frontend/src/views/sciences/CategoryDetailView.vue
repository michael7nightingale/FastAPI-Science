<template>
  <div class="body-content">
    <ul role="list" class="divide-y divide-gray-100">
      <li class="flex justify-between gap-x-6 py-5" v-for="formula in categoryData.formulas" v-bind:key="formula.id">
        <router-link :to="{name: 'formula', params: {slug: formula.slug}}" class="flex min-w-0 gap-x-4">
          <img class="h-12 w-12 flex-none rounded-full bg-gray-50"
               src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
               alt="">
          <div class="min-w-0 flex-auto">
            <p class="text-sm font-semibold leading-6 text-gray-900">{{ formula.title }}</p>
          </div>
        </router-link>
        <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
          <p class="text-sm leading-6 text-gray-900">{{formula.formula}}</p>
          <div>
            <!--          <vue-mathjax formula="$$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.$$"></vue-mathjax>-->
          </div>
          <!--          <div class="demo-container">-->
          <!--              <textarea v-model="formula_" cols="30" rows="10"></textarea>-->
          <!--              <vue-mathjax :key="formula_" :formula="formula_"></vue-mathjax>-->
          <!--          </div>-->
          <p class="mt-1 text-xs leading-5 text-gray-500">Last seen
            <time datetime="2023-01-23T13:23Z">3h ago</time>
          </p>
        </div>
      </li>
    </ul>
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
  },

}
</script>

<style scoped>
@import "../../../node_modules/katex/dist/katex.min.css";
@import '../../assets/css/sciences.css';
</style>