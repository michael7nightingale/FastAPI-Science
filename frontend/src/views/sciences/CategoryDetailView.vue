<script>
import {getCategoryDetail} from "/src/services/ScienceService";

export default {
  name: "CategoryDetailView",
  data(){
    return {
      science: {slug: 'ps'},
      formulas: [],
      category: {},
    }
  },
  mounted() {
    let promise = getCategoryDetail(this.$route.params.slug)
    promise.then(response => {
      this.category = response.category;
      this.formulas = response.formulas;
      this.science = response.science;
      console.log(this.science)
    });

  }

}
</script>


<template>
 <div class="jumbotron">
    <h2>{{ category.title }}</h2>
    <p class="lead">{{ category.content }}</p>
<!--    <link rel="stylesheet" href="{{ url_for('static', path='sciences/css/category.css') }}">-->
<!--    <router-link :to="{name: 'science', params: {slug: science.slug}}" class="btn btn-primary btn-large">назад к {{ science.title }} &raquo;</router-link>-->
</div>
    <h3 align="center" class="white_text">Formulas</h3>
    <div class="row">
      <div class="col" style="background-color: #b2b3b4">
        <ul>
            <h4 align="center">Contains</h4>
                <li v-for="formula in formulas" v-bind:key="formula">
                <router-link class="" :to="{name: 'formula', params: {slug: formula.slug}}">
                     <p class="">{{ formula.title }}</p>
                 </router-link>
                </li>
        </ul>

        </div>
      <div class="col">
<!--             {% for row_idx in range((formulas|length // 3) + 1) %}-->
<!--                 <div class="row">-->
<!--                 {% for col_idx in range(0, 3) %}-->
<!--                    {% if row_idx * 3 + col_idx < formulas|length %}-->
<!--                    <div class="col">-->
<!--                        <div class="formula" style="background-color: white; padding: 5px; margin-bottom: 20px">-->
<!--                            <a class="" href="{{ url_for('formula_get', formula_slug=formulas[row_idx * 3 + col_idx].slug) }}">-->
<!--                                 <h5 style="color: black">{{ formulas[row_idx * 3 + col_idx].formula }}</h5>-->
<!--                             </a>-->
<!--                        </div>-->
<!--                    </div>-->
<!--                    {% else %}-->
<!--                        <div class="col"></div>-->
<!--                    {% endif %}-->
<!---->
<!--                 {% endfor %}-->
<!--                 </div>-->
<!--            {% endfor %}-->
        </div>
     </div>

</template>


<style scoped>
.f_content{
    background-color: #b2b3b4;
}

</style>