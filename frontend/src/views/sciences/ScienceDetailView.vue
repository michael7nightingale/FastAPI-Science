<script>
import {getScienceDetail} from "/src/services/ScienceService";

export default {
  name: "SciencesDetailView",
  data(){
    return {
      science: {},
      categories: [],
    }
  },
  mounted() {
    console.log(this.$route.params.slug);
    let promise = getScienceDetail(this.$route.params.slug)
    promise.then(response => {
      this.science = response.science;
      this.categories = response.categories;
    });

  }

}
</script>



<template>
     <div class="jumbotron">
         <h2>{{ science.title }}</h2>
         <p class="lead">&nbsp;{{ science.content }}</p>
      <router-link to="/sciences" class="btn btn-primary btn-large">назад к наукам &raquo;</router-link>
</div>

    <div class="container">
      <div class="category-col row" v-for="category in categories" v-bind:key="category">
            <div class="col-3">
                <div class="row">
<!--                    {% if i.image_path %}-->
<!--                   <img src="{{ url_for('static', path=category.image_path) }}" width="130">-->
<!--                    {% endif %}-->
                </div>
            </div>
            <div class="col">
                <div class="row">
                    <h4 align="center">
                    <router-link :to="{name: 'category', params: {slug: category.slug}}">{{ category.title  }}</router-link>
                    </h4>
                </div>

                <div class="row">
                    <p>{{ category.content.slice(0, 100) }}</p>
                </div>
            </div>

            </div>
      </div>
</template>



<style scoped>
.science-container{
    margin-bottom: 50px;
    background: #dddddd;
    padding: 10px;
    align-content: center;

.category-col{
  background-color: #ececec;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 5%;

}
}
</style>