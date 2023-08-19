<script>
import {getScienceList} from "/src/services/ScienceService";

export default {
  name: "SciencesListView",
  data(){
    return {
      sciences: []
    }
  },
  mounted() {
    let promise = getScienceList()
    promise.then(response => this.sciences = response);

  }

}
</script>



<template>
<div class="jumbotron">
    <h1>Раздел наук</h1>
</div>

<div class="row">
    <div class="col science-col" v-for="science in sciences" v-bind:key="science">
<!--        {% if i.image_path %}-->
<!--        <img src="{{ url_for('static', path="sciences/" + i.image_path) }}" width=30% height=60%>-->
<!--        {% endif %}-->
        <h2>{{ science.title }}</h2>
        <p>
            {{ science.content.slice(0, 50) }}
        </p>
        <router-link class="btn btn-outline-primary text" :to="{name: 'science', params: {slug: science.slug}}">перейти &raquo;</router-link>
    </div>

</div>
</template>



<style scoped>
.science-col{
  background-color: dodgerblue;
  height: 100%;
  padding: 20px;
  border-radius: 10px;
  margin-left: 5%;

}
</style>