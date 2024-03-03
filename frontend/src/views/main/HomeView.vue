<template>
  <section class="backgroun relative overflow-hidden">
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
    <h2 class="title">
      Науки
    </h2>
    <div class="science-card-wrapper">
      <div class="science-card">
        <img :src="'/images/logo.png'"/>
        <h3>математика</h3>
      </div>
      <div class="science-card">
        <img :src="'/images/logo.png'"/>
        <h3>Физика</h3>
      </div>
      <div class="science-card">
        <img :src="'/images/logo.png'"/>
        <h3>Химия</h3>
      </div>
      <div class="science-card">
        <img :src="'/images/logo.png'"/>
        <h3>Биология</h3>
      </div>
    </div>
  </section>
</template>

<script>

export default {
  name: 'HomeView',
  components: {}
}
</script>


<style>
@import '../../assets/css/home.css';
</style>