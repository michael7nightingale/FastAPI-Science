<script>
import {getSpecialCategoryDetail, postPlot} from "/src/services/ScienceService";

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

    downloadPlot(){

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
      <h2>Графики функций</h2>
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

  <div class="row" style="margin: 20px">
     <img v-if="plotPath" :src="plotUrl()" style="width: 100%">
      <input class="" type="text" placeholder="Скачать как:">
      <button @click="downloadPlot">Скачать</button>
  </div>

</div>
</template>


<style>
#faq {
  margin: 10px;
  text-align: center;
}

section.faq {
  padding-top: 2em;
  padding-bottom: 3em;
}

#faq ul {
  text-align: left;
}
.transition, p, ul li i:before, ul li i:after {
  transition: all 0.3s;
}

#faq .no-select, #faq h2 {
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
  user-select: none;
}

#faq h1 {
  color: #000;
  margin-bottom: 30px;
  margin-top: 0;
}

#faq h2 {
  color: #cc071e;
  font-family: 'hm_light', sans-serif;
  font-size: 20px;
  line-height: 34px;
  text-align: left;
  padding: 15px 15px 0;
  text-transform: none;
  font-weight: 300;
  letter-spacing: 1px;
  display: block;
  margin: 0;
  cursor: pointer;
  transition: .2s;
}

#faq p {
  color: #333;
  text-align: left;
  font-family: 'hm_light', sans-serif;
  font-size: 17px;
  line-height: 1.45;
  position: relative;
  overflow: hidden;
  max-height: 250px;
  will-change: max-height;
  contain: layout;
  display: inline-block;
  opacity: 1;
  transform: translate(0, 0);
  margin-top: 5px;
  margin-bottom: 15px;
  padding: 0 50px 0 15px;
  transition: .3s opacity, .6s max-height;
  hyphens: auto;
  z-index: 2;
}

#faq ul {
  list-style: none;
  perspective: 900;
  padding: 0;
  margin: 0;
}
#faq ul li {
  position: relative;
  overflow: hidden;
  padding: 0;
  margin: 0;
  /*padding-bottom: 4px;*/
  /*padding-top: 18px;*/
  background: #fff;
  box-shadow: 0 3px 10px -2px rgba(0,0,0,0.1);
  -webkit-tap-highlight-color: transparent;
}
#faq ul li + li {
  margin-top: 15px;
}
#faq ul li:last-of-type {
  padding-bottom: 0;
}
#faq ul li i {
  position: absolute;
  transform: translate(-6px, 0);
  margin-top: 28px;
  right: 15px;
}
#faq ul li i:before, ul li i:after {
  content: "";
  position: absolute;
  background-color: #cc071e;
  width: 3px;
  height: 9px;
}
#faq ul li i:before {
  transform: translate(-2px, 0) rotate(45deg);
}
#faq ul li i:after {
  transform: translate(2px, 0) rotate(-45deg);
}
#faq ul li input[type=checkbox] {
  position: absolute;
  cursor: pointer;
  width: 100%;
  height: 100%;
  z-index: 1;
  opacity: 0;
  touch-action: manipulation;
}
#faq ul li input[type=checkbox]:checked ~ h2 {
  color: #000;
}
#faq ul li input[type=checkbox]:checked ~ p {
  /*margin-top: 0;*/
  max-height: 0;
  transition: .3s;
  opacity: 0;
  /*transform: translate(0, 50%);*/
}
#faq ul li input[type=checkbox]:checked ~ i:before {
  transform: translate(2px, 0) rotate(45deg);
}
#faq ul li input[type=checkbox]:checked ~ i:after {
  transform: translate(-2px, 0) rotate(-45deg);
}











* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
}

a,
a:visited,
a:focus,
a:active,
a:link {
  text-decoration: none;
  outline: 0;
}

a {
  color: currentColor;
  transition: .2s ease-in-out;
}

h1, h2, h3, h4 {
  margin: .3em 0;
}

ul {
  padding: 0;
  list-style: none;
}

img {
  vertical-align: middle;
  height: auto;
  width: 100%;
}
</style>