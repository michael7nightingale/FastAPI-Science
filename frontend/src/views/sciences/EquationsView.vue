<script>
import { getSpecialCategoryDetail, postEquations} from "@/services/ScienceService";

export default {
  "name": "EquationsView",
  data(){
    return {
      storage: [""],
      science: {},
      category: {},
      result: []
    }
  },

  mounted() {
    let promise = getSpecialCategoryDetail(this.$route.name)
    promise.then(response => {
      this.category = response.category;
      this.science = response.science;
      this.plotPath = response.plotPath
    })

  },

  methods: {

    buildPlot(){
      let data = {}
      let number = 1
      for (let functionValue of this.storage){
        data[`equation${number}`] = functionValue;
        number += 1
      }
        postEquations(data)
            .then((response) => {
              let message = response.detail;
              if (message){
                alert(message)
              }
              else{
                this.result = response.result
              }
            })
            .catch((error) => {
              error
              alert("You are not authorized!")
              this.$router.push("/auth/login")
            })
    },

    inputFunction(value, name){
      this.storage[name] = value;
    },

    addFunction(){
      let storageProxy = this.storage;
       storageProxy.push("");
       this.storage = storageProxy;
    },

    deleteFunction(idx){
       let storageProxy = this.storage;
       storageProxy.splice(idx, 1);
       this.storage = storageProxy;
    },
  },

}
</script>

<template>
<div class="jumbotron">
  <div id="faq">
  <ul>
    <li>
      <input type="checkbox" checked>
      <h2>{{ category.title }}</h2>
    <p class="lead">{{ category.content }}</p>
    </li>
  </ul>
  </div>

    <router-link :to="`/science/${science.slug}`" class="btn btn-primary btn-large">назад к {{ science.title }} &raquo;</router-link>
</div>

<div class="container">
  <div class="form-item">
    <button class="btn btn-primary" @click="addFunction()">
      + Add
    </button>
  </div>
  <div class="row" v-for="n in Array(storage.length).keys()" :key="n">
    <div class="col">
      <input
      class="form-control form-item"
      type="text"
      :value="storage[n]"
      @input="inputFunction($event.target.value, n)"
      :placeholder="`Уравнение ${n + 1}`"
      />
    </div>
    <div class="col-2">
      <button class="btn btn-primary form-item" style="background-color: red"
        @click="deleteFunction(n)">
        Удалить
      </button>
    </div>
  </div>

  <div class="row" style="margin: 20px">
    <div class="col">
       <button class="btn btn-primary" @click="buildPlot">Решить</button>
    </div>
  </div>

  <div style="background-color: white">
    <h4 v-for="(data, key) in result" :key="key">{{ key }} = {{ data }}</h4>
  </div>
</div>
</template>

<style scoped>

</style>