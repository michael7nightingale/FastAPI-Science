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
      for (let l in this.info.literals){
        this.findMark = this.info.literals[l].literal;
        break;
      }

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
      console.log(this.storage)
  },

  numsCommaSelect(event){
      this.storage.numsComma = event.target.value;
  },

  siSelect(event, literal){
      this.storage[literal + 'si'] = event.target.value;
  },

  countResult(){
      let result;
      countResult(this.$route.params.slug, this.storage, this.numsComma, this.findMark)
          .then(responseData => {
            result = responseData.result;
            this.result = result;
          })

  }

 }

}
</script>

<template>
    <div class="jumbotron">
    <h2>{{ formula.title }}</h2>
    <p class="lead">{{ category.title }}</p>
    <a href="}" class="btn btn-primary btn-large">назад к  &raquo;
        {{ category.title }}
    </a>
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
        <input type="text" :placeholder="`${literal.literal} =`" class="form-control" @input="numberInput($event, literal.literal)">
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
              :selected="ed === 1 ? '' : 'selected'"
          >
            {{ name }}
          </option>
        </select>
        </div>
    </div>

  <button
    class="btn btn-primary"
    @click="countResult"
  >
  Считать
  </button>
  <h4>{{ findMark }} = {{ result }}</h4>
  </div>
</div>


<div style="">
<p class="lead">{{ formula.content }}</p>
</div>

</template>

<style scoped>
/* Style the tab */
.tab {
  float: left;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
  width: 30%;
  height: 300px;
}

/* Style the buttons that are used to open the tab content */
.tab button {
  display: block;
  background-color: inherit;
  color: black;
  padding: 22px 16px;
  width: 100%;
  border: none;
  outline: none;
  text-align: left;
  cursor: pointer;
  transition: 0.3s;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current "tab button" class */
.tab button.active {
  background-color: #ccc;
}

.input{
  background: rosybrown;
}

/* Style the tab content */
.tabcontent {
  float: left;
  padding: 0px 12px;
  border: 1px solid #ccc;
  width: 70%;
  border-left: none;
  height: 300px;
}

</style>
