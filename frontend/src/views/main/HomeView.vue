<template>
  <section class="relative overflow-hidden">
    <div class="hero-image"></div>
    <div class="relative mt-4">
      <h1 class="hero-title">
        Сайт для вычислений
      </h1>
      <div class="flex hero-text-container gap-5">
        <div class="hero-text-block">
          Группа компаний «Интерстилс» поставляет металлопродукцию по всей России и странам СНГ. Обширный опыт работы с
          клиентами и поставщиками из России, Китая и Европы, развитая сеть филиалов, а также собственный автопарк
          позволяют нам подобрать соответствующее решение даже для нестандартных проектов. Вся продукция изготовлена по
          ГОСТам и ТУ и имеет все необходимые сертификаты качества, потому что мы стремимся к долгосрочному
          сотрудничеству с нашими клиентами.
        </div>
        <div class="col-lg hero-text-block">
          ГК «Интерстилс» — это квалифицированные специалисты, которые в течение одного часа обработают вашу заявку,
          подберут необходимые товары и решат все задачи по транспортировке.

          Мы предлагаем самые выгодные цены на металлопродукцию, потому что работаем напрямую с производителями, а также
          постоянно следим за рынком и предоставляем целую систему скидок для крупных заказов и постоянных клиентов.
        </div>
      </div>
    </div>
  </section>
  <section class="px-5">
    <h2 class="text-3xl text-center mt-8  font-bold">
      Науки
    </h2>
    <div class="grid grid-cols-1 gap-2 mt-3 sm:grid-cols-3 lg:mt-20">
      <router-link v-for="science in sciences" v-bind:key="science.id" :to="{name: 'science', params: {slug: science.slug}}"
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
import {buildStaticUrl} from "@/services/Base";
import {defineComponent} from "vue";

export default defineComponent({
  methods: {buildStaticUrl}

})

</script>


<style>
@import '../../assets/css/home.css';
</style>