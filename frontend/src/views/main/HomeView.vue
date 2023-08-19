<template>
  <div class="home">

  <div class="jumbotron">
      <h1>Сайт для физико-математических вычислений</h1>
  </div>

  <div class="row">
      <div class="block col-md-4">
          <h2>Науки и формулы</h2>
          <p>
             счет по формулам
          </p>
          <router-link class="btn btn-outline-primary text" to="/sciences">перейти &raquo;</router-link>
      </div>
      <div class="block col-md-4">
          <h2>Задачи и решения</h2>
          <p>
             Помогайте другим разваваться и развивайтесь сами
          </p>
          <router-link class="btn btn-outline-primary text" to="/problems">перейти &raquo;</router-link>
      </div>
  </div>

  </div>
</template>

<script>

export default {
  name: 'HomeView',
  components: {

  }
}
</script>


<style>
.block{
  background-color: #ececec;
  padding: 20px;
  border-radius: 10px;
  margin-left: 5%;

}

</style>