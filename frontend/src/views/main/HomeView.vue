<template>
  <section class="relative overflow-hidden">
    <div class="hero-image"></div>
    <div class="relative mt-4">
      <h1 class="hero-title">
        Сайт для вычислений
      </h1>
      <div class="flex hero-text-container gap-5">
        <div class="hero-text-block">
          В современном мире сфера научных исследований и инженерных разработок становится все более востребованной и
          стремительно развивается. Однако, для успешной работы в этой области необходимы доступные вычислительные
          инструменты, специализированные программные средствам и инфраструктура.
        </div>
        <div class="col-lg hero-text-block">
          Создание специализированного веб-ресурса для физико-математических вычислений становится актуальной задачей,
          которая позволит обеспечить ученых, инженеров и студентов необходимыми инструментами для проведения научных
          расчетов, анализа данных, моделирования и работы с математическими методами и моделями.
        </div>
      </div>
    </div>
  </section>
  <section class="px-5">
    <h2 class="text-3xl text-center mt-8  font-bold">
      Науки
    </h2>
    <div class="grid grid-cols-1 gap-2 mt-3 sm:grid-cols-3 lg:mt-20">
      <router-link v-for="science in sciences" v-bind:key="science.id"
                   :to="{name: 'science', params: {slug: science.slug}}"
                   class="transition-all  duration-1000 bg-blue-500 hover:bg-blue-700 hover:shadow-xl m-2 p-4 relative group  ">
        <div
            class=" absolute bg-blue-500/50 top-0 left-0 w-24 h-1 z-30  transition-all duration-200 group-hover:bg-white group-hover:w-1/2  ">
        </div>
        <div class="py-2 px-9 relative  ">
          <img class="w-40 h-40" :alt="science.title" :src="buildStaticUrl(`sciences/${science.image_path}`)">
          <h3 class="mt-8 text-lg font-semibold text-black group-hover:text-white ">
            {{ science.title }}
          </h3>
          <p class="mt-4 text-base text-gray-600 group-hover:text-white"></p>
        </div>
      </router-link>
    </div>
  </section>
</template>

<script>
import {getScienceList} from "@/services/ScienceService";
import {buildStaticUrl} from "@/services/Base";

export default {
  name: 'HomeView',
  methods: {buildStaticUrl},
  components: {},
  data() {
    return {
      sciences: []
    }
  },
  mounted() {
    let promise = getScienceList()
    promise.then(response => this.sciences = response)
  }
}
</script>


<style>
@import '../../assets/css/home.css';
</style>