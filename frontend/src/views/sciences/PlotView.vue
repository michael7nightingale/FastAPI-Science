<script>
import {downloadPlot, getSpecialCategoryDetail, postPlot} from "/src/services/ScienceService";


export default {
  name: "SciencesDetailView",
  data(){
    return {
      science: {},
      category: {},
      functionsAmount: 4,
      xMin: -100,
      xMax: 100,
      yMin: 100,
      yMax: 100,
      plotPath: null,
      storage: {},
      filename: "plot",

    }
  },
  mounted() {
    let promise = getSpecialCategoryDetail(this.$route.name)
    promise.then(response => {
      this.category = response.category;
      this.science = response.science;
      this.plotPath = response.plotPath
    });

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
      this.storage.xMin = this.xMin;
      this.storage.xMax = this.xMax;
      this.storage.yMax = this.yMax;
      this.storage.yMin = this.yMin;
        postPlot(this.storage)
            .then((response) => {
              let message = response.detail;
              if (message){
                alert(message)
              }
              else{
                this.plotPath = response.plotPath
              }
            })
    },

    downloadClick(){
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
    },

    inputFunction(value, name){
      this.storage[name] = value;
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
  <input
      v-for="n in Array(functionsAmount).keys()"
      v-bind:key="n"
      class="form-control"
      type="text"
      @input="inputFunction($event.target.value, `function${n + 1}`)"
      :placeholder="`Функция ${n + 1}`"
  />
  <input class="form-control" type="number" :value="xMin" @click="xMinInput($event.target.value)" placeholder="x min">
  <input class="form-control" type="number" :value="xMax" @click="xMaxInput($event.target.value)" placeholder="x max">
  <input class="form-control" type="number" :value="yMin" @click="yMinInput($event.target.value)" placeholder="y min">
  <input class="form-control" type="number" :value="yMax" @click="yMaxInput($event.target.value)" placeholder="y max">
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

</style>