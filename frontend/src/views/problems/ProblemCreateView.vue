<script>
import {getScienceList} from "@/services/ScienceService";
import {createProblem} from "@/services/ProblemService";

export default {
  name: "ProblemCreateView",
  data(){
    return{
        medias: [],
        sciences: [],
        title: null,
        text: null,
        science: null
    }
  },

  methods: {
    addMedia(){
       let mediasProxy = this.medias;
       if (!mediasProxy.length || mediasProxy[mediasProxy.length - 1]){
          mediasProxy.push(null);
       this.medias = mediasProxy;
       }
        else{
          alert("Media is unfilled.")
       }
    },

    deleteMedia(index){
       let mediasProxy = this.medias;
       mediasProxy.splice(index, 1);
       this.medias = mediasProxy;
    },

    mediaInput(value, index){
       let mediasProxy = this.medias;
       mediasProxy[index] = value;
       this.medias = mediasProxy;
    },

    createButtonClick(){
      let data = {
        title: this.title,
        text: this.text,
        medias: this.medias,
        science_id: this.science,

      };
      createProblem(data);

    },

  },

  mounted() {
      getScienceList()
        .then((data) => {
          this.sciences = data;
        });

  }


}
</script>


<template>
<div class="jumbotron">
    <h2>Создание проблемы</h2>
    <p class="lead"></p>
    <div class="row">
       <div class="col-2">
            <router-link :to="{name: 'problems'}" class="btn btn-primary btn-large">назад к проблемам &raquo;</router-link>
       </div>
    </div>
</div>

<div class="container">
    <label for="title" class="white_text">Заголовок</label>
    <input type="text" id="title" class="form-control" placeholder="Title" required="required"
           :value="title"
           @input="($event) => {title = $event.target.value; }"
    >
    <label for="text" class="white_text margin-top" >Текст</label>
    <textarea required="required" class="form-control" placeholder="Text" id="text" v-model="text"></textarea>
    <label for="science" class="white_text margin-top">Наука</label>
    <div class="row">
        <select required="required" class="form-control" v-model="science" id="science">
          <option v-for="s in sciences" v-bind:key="s" :value="s.slug">{{ s.title }}</option>
       </select>
    </div>

  <button class="btn btn-primary btn-large margin-top margin-bottom" @click="addMedia">+ Добавить медиа</button>
  <div id="medias">
    <div class="row" v-for="(media, index) in medias" v-bind:key="index">
      <div class="col">
        <input class="form-control" type="file" @input="mediaInput($event.target.value, index)" name="media1" placeholder="Choose media" id="input-media-1">
      </div>
      <div class="col">
        <button class="delete-button" id="button-delete-1" @click="deleteMedia(index)">Удалить</button>
      </div>
    </div>
  </div>
  <div class="row" style="margin: 20px">
    <div class="col">
      <button class="btn btn-primary btn-large margin-top margin-bottom" @click="createButtonClick">Создать</button>
    </div>
  </div>
</div>
</template>


<style scoped>
@import '../../assets/css/problems.css';
</style>