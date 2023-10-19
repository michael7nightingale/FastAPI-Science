<script>
import {countResult, getFormulaDetail} from "/src/services/ScienceService";

export default {
  name: "CategoryDetailView",
  data(){
    return {
      formula: [],
      category: {},
      info: {},
      result: null,
      findMark: null,
      numsComma: [10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      storage: {}
    }
  },
  mounted() {
    let promise = getFormulaDetail(this.$route.params.slug)
    promise.then(response => {
      this.category = response.category;
      this.formula = response.formula;
      this.info = response.info;
      let info = JSON.parse(JSON.stringify(this.info));
      this.info = info;
      this.findMark = Object.keys(info.literals)[0];
    })
    .then(() => {
       document.getElementById("loader").className = document.getElementById("loader").className.replace("show", "hide")
       document.getElementById("main").className = document.getElementById("main").className.replace("hide", "show")
    });

  },
  methods: {
    tabClick(event, literal){
        let i, tablinks;
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        this.findMark = literal;
        event.target.className += " active";

    },

  numberInput(event, literal){
      this.storage[literal] = event.target.value;
  },

  numsCommaSelect(event){
      this.storage.numsComma = event.target.value;
  },

  siSelect(event, literal){
      this.storage[literal + 'si'] = event.target.value;
  },

  getLiteralsExceptFindMark(){
      let literals = [];
      for (const literal of Object.keys(this.info.literals)){
        if (literal !== this.findMark){
          literals.push(literal);
        }
      }
      return literals;
  },

  checkStorage(){
      let neededLiterals = this.getLiteralsExceptFindMark();
      let isCorrectData = true;
      for (const literal of neededLiterals){
        if (!(this.storage[literal] && this.storage[`${literal}si`])){
          isCorrectData = false;
          document.getElementById(`${literal}-text-danger`).innerText = "Заполните поле"
        }
      }
      return isCorrectData;
  },

  countResult(){
      let result;
      let count = this.checkStorage();
      if (count){
          countResult(this.$route.params.slug, this.storage, this.numsComma, this.findMark)
          .then(responseData => {
            result = responseData.result;
            this.result = result;
          })
         .catch((error) => {
              error
              alert("Авторизуйтесь, чтобы воспользоваться функцией вычислений");
              this.$router.push({name: "login"});
            })
      }

  }

 }

}
</script>

<template>
<div class="centered show" id="loader">
  <span class="loader"></span>
</div>
<div class="hide" id="main">
 <div class="jumbotron">
    <div id="faq">
   <ul>
     <li>
       <input type="checkbox" checked>
       <h3 style="text-align: center">{{ formula.title }}</h3>
     <p class="lead">{{ formula.content }}</p>
     </li>
   </ul>
   </div>
 <router-link :to="{name: 'category', params: {slug: category.slug}}" class="btn btn-primary btn-large">назад к  &raquo;
     {{ category.title }}
 </router-link>
</div>

<div class="tab" style="min-height: 400px;">
  <div v-for="literal in this.info.literals" v-bind:key="literal">
    <button
        :class="literal.literal === findMark ? 'tablinks active' : 'tablinks'"
        @click="tabClick($event, literal.literal)"
        v-if="!(literal.is_constant)">
          Найти {{ literal.literal }}
    </button>
  </div>

</div>

<div class="container" style="min-height: 400px;">
  <div id="{{ findMark }}" class="tabcontent">
  <label for="nums_comma">Цифр после запятой: </label>
  <select title="nums_comma" name="nums_comma" id="nums_comma" @change="numsCommaSelect($event)">
    <option
        v-for="n in numsComma"
        :value="n"
        v-bind:key="n"
    >
      {{ n }}
    </option>
  </select>

    <div v-for="literal in this.info.literals" v-bind:key="literal">
       <div class="form"  style="{min-height: 400px}" v-if="literal.literal !== findMark">
         <label :for="`${literal.literal}si`">Ед.измерения:</label>
        <select
            :id="`${literal.literal}si`"
            @change="siSelect($event, literal.literal)"
            v-model="storage[`${literal.literal}si`]"
        >
          <option
              v-for="(ed, name) in literal.si"
              v-bind:key="ed"
              :value="name"
              :selected="ed === '1' ? '' : 'selected'"
          >
            {{  ed === 1 ? storage[`${literal.literal}si`] = name : name  }}
          </option>
        </select>
        <input
            type="text"
            :placeholder="`${literal.literal} =`"
            class="form-control"
            @input="numberInput($event, literal.literal)"
            :value="storage[literal.literal]"
        >
         <p class="text-danger text-margin" :id="`${literal.literal}-text-danger`"></p>

        </div>
    </div>

    <button
      class="btn btn-primary button-blue"
      @click="countResult"
    >
    Считать
    </button>
    <h3 class="text-margin">{{ findMark }} = {{ result }}</h3>
    </div>
  </div>
</div>
</template>

<style scoped>
@import '../../assets/css/sciences.css';
</style>
