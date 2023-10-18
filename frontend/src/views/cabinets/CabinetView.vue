<script>
import {getUser} from "@/services/Auth";

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
  },
  mounted() {
    let user = getUser();
    if (!user){
      window.location = this.$router.resolve({name: "login"}).fullPath;
    }
  }

}
</script>

<template>
 <div class="jumbotron">
        <h2 @click="getUser">Личный кабинет - {{ User.username }}</h2>
        <p class="lead">Смотрите журнал вычислений и многое другое.</p>
        <router-link :to="{name: 'homepage'}" class="btn btn-primary btn-large">назад на главную &raquo;</router-link>
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