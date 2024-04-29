<script>
import {getScienceDetail} from "/src/services/ScienceService";
import {buildStaticUrl} from "@/services/Base";

export default {
  name: "SciencesDetailView",
  methods: {buildStaticUrl},
  data() {
    return {
      scienceData: {},
    }
  },
  mounted() {
    let promise = getScienceDetail(this.$route.params.slug)
    promise.then(response => {
      this.scienceData = response;
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
          <span class="text-gray-800">{{ scienceData.title }}</span>
        </li>
      </ol>
    </nav>
    <div class="grid grid-cols-1 gap-8 mt-3 sm:grid-cols-3 lg:mt-20">
      <div v-for="category in scienceData.categories" v-bind:key="category.id">
        <router-link v-if="category.is_special" :to="`/special-category/${category.slug}/`" class="flex min-w-0 gap-x-4">
          <img class="h-20 w-20 flex-none rounded-full bg-gray-50"
               :src="buildStaticUrl(`sciences/${category.image_path}`)"
               :alt="category.title">
          <div class="min-w-0 flex-auto">
            <p class="text-sm font-semibold leading-6 text-gray-900">{{category.title}}</p>
            <p class="mt-1 truncate text-xs leading-6 text-blue-800">Спецкатегория</p>
          </div>
        </router-link>
        <router-link v-else :to="{name: 'category', params: {slug: category.slug}}" class="flex min-w-0 gap-x-4">
          <img class="h-20 w-20 flex-none rounded-full bg-gray-50"
               :src="buildStaticUrl(`sciences/${category.image_path}`)"
               :alt="category.title">
          <div class="flex-auto">
            <p class="text-sm font-semibold leading-6 text-gray-900">{{category.title}}</p>
            <p class="mt-1 truncate text-xs leading-5 text-gray-500">формул: {{category.formulas_count}}</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../../assets/css/sciences.css';
</style>