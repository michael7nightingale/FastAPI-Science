<script>
import {downloadPlot, getSpecialCategoryDetail, postPlot} from "/src/services/ScienceService";


export default {
  name: "PlotView",
  data(){
    return {
      science: {},
      category: {},
      xMin: -100,
      xMax: 100,
      yMin: 100,
      yMax: 100,
      plotPath: null,
      storage: [""],
      filename: "plot",

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
    xMaxInput(value){
      this.xMax = value;
    },
    xMinInput(value){
      this.xMin = value;
    },
    yMaxInput(value){
      this.yMax = value;
    },
    yMinInput(value){
      this.yMin = value;
    },

    filenameInput(value){
      this.filename = value;
    },

    buildPlot(){
      let data = {}
      data.xMin = this.xMin;
      data.xMax = this.xMax;
      data.yMax = this.yMax;
      data.yMin = this.yMin;
      let number = 1
      for (let functionValue of this.storage){
        data[`function${number}`] = functionValue;
        number += 1
      }
        postPlot(data)
            .then((response) => {
              let message = response.detail;
              if (message){
                alert(message)
              }
              else{
                this.plotPath = response.plotPath
              }
            })
            .catch((error) => {
              error
              alert("You are not authorized!")
              this.$router.push("/auth/login")
            })
    },

    downloadClick(){
        if (this.plotPath){
               downloadPlot(this.filename)
            .then((response) => {
              console.log(response.status)
               const blob = new Blob([response.data], { type: `application/png` });
               const link = document.createElement("a");
               link.href = URL.createObjectURL(blob);
               link.download = `${this.filename}.png`;
               link.click();
               URL.revokeObjectURL(link.href);
            })
        }
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

    plotUrl(){
      return "http://localhost:8001/static/".concat(this.plotPath)
    }

  }

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
      :placeholder="`Функция ${n + 1}`"
      />
    </div>
    <div class="col-2">
      <button class="btn btn-primary form-item" style="background-color: red"
        @click="deleteFunction(n)">
        Удалить
      </button>
    </div>
  </div>

  <div class="row form-item">
    <div class="col-2">
        <label for="x-min" style="color: white">X min</label>
    </div>
    <div class="col">
      <input class="form-control" id="x-min" type="number" :value="xMin" @click="xMinInput($event.target.value)" placeholder="x min">
    </div>
  </div>

  <div class="row form-item">
    <div class="col-2">
        <label for="x-max" style="color: white">X max</label>
    </div>
    <div class="col">
      <input class="form-control" id="x-max" type="number" :value="xMax" @click="xMaxInput($event.target.value)" placeholder="x max">
    </div>
  </div>

  <div class="row form-item">
    <div class="col-2">
        <label for="y-min" style="color: white">Y min</label>
    </div>
    <div class="col">
      <input class="form-control" id="y-min" type="number" :value="yMin" @click="yMinInput($event.target.value)" placeholder="y min">
    </div>
  </div>

  <div class="row form-item">
    <div class="col-2">
        <label for="y-max" style="color: white">Y max</label>
    </div>
    <div class="col">
      <input class="form-control" id="y-max" type="number" :value="yMax" @click="yMaxInput($event.target.value)" placeholder="y max">
    </div>
  </div>

  <div class="row" style="margin: 20px">
    <div class="col">
       <button class="btn btn-primary" @click="buildPlot">Построить график</button>
    </div>
  </div>

  <div>

  </div>
  <div v-if="plotPath">
    <img v-if="plotPath" :src="plotUrl()" style="width: 100%">
    <div class="row" style="margin: 20px">
      <div class="col">
         <input class="form-control" type="text" placeholder="Скачать как:" :value="filename" @input="filenameInput($event.target.value)">
      </div>
      <div class="col">
        <button class="btn btn-primary button-blue" style="margin: 0px" @click="downloadClick">Скачать</button>
      </div>
    </div>
  </div>

</div>
</template>


<style>
.form-item{
  margin: 15px;
}
</style>