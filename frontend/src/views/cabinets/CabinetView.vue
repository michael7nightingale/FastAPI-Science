<script>
export default {
  name: "CabinetView",
  data() {
    return {

    }
  },


  computed: {
      User(){
        return JSON.parse(localStorage.userData);
      }
  }

}
</script>

<template>
 <div class="jumbotron">
        <h2 @click="getUser">Личный кабинет - {{ User.username }}</h2>
        <p class="lead">Смотрите журнал вычислений и многое другое.</p>
        <a href="/" class="btn btn-primary btn-large">назад на главную &raquo;</a>
        <a href="/docs" class="btn btn-primary btn-large">документация &raquo;</a>
    </div>

    <div class="container">
        <div class="row">
            <div class="col">
            <button class="btn btn-primary btn-large">
                      <router-link class="white_text" to="/cabinet/history"><h4>История вычислений</h4></router-link>
            </button>
            </div>
            <div class="col">
            <button class="btn btn-primary btn-large">
                <a class="white_text" href=""><h4>Предложить формулу</h4></a>
            </button>
             </div>
        </div>

    </div>
</template>

<style>

</style>