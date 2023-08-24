<script>
import {getScienceList} from "@/services/ScienceService";
import {getProblemsList} from "@/services/ProblemService";

export default {
  name: "ProblemsListView",
  data(){
    return  {
      sciences: [],
      problems: [],
      filters: {
        sciences: [],
        isSolved: true
      },
      filtersOpened: false,
      filtersButtonText: "Open filters >>",

    }
  },
  methods: {
    scienceFilterCheckboxChange(el, scienceSlug){
      let filterSciencesProxy = this.filters.sciences;
      if (filterSciencesProxy.includes(scienceSlug)){
         filterSciencesProxy.splice(filterSciencesProxy.indexOf(scienceSlug), 1)
      }
      else{
        filterSciencesProxy.push(scienceSlug);
      }

    },

    moveFilters(){
      this.filtersOpened = !this.filtersOpened;

    }
  },

  mounted() {
    getScienceList()
        .then((data) => {
          this.sciences = data;
        });

    getProblemsList()
        .then((response) => {
          this.problems = response.data;
        });

  }
}
</script>


<template>
<div class="jumbotron">
         <h2>Problems</h2>
         <p class="lead">Solve science problems together.</p>
         <div class="row">
           <router-link :to="{name: 'homepage'}" class="btn btn-primary btn-large">назад на главную &raquo;</router-link>
           <router-link :to="{name: 'problem-create'}" class="btn btn-primary btn-large">create &raquo;</router-link>
         </div>

</div>

     <div class="row">
     <div class="col">
         <button class="btn btn-primary btn-large" @click="moveFilters">{{ filtersButtonText }}</button>
     </div>
     </div>

    <div class="filters" :style="filtersOpened ? `display:block` : 'display:none;'" id="filters">
         <h3 align="center">Filters</h3>
            <div class="row">
                <div class="col">
                      <label for="sciences-cell-titles ">Sciences</label>
                  <div id="sciences-cell-titles margin-top">
                    <div v-for="science in sciences" v-bind:key="science">
                      <label :for="science.slug">{{ science.title }}</label>
                      <input type="checkbox" onchange="scienceFilterCheckboxChange($event.target, science.slug)" :id="science.slug" :name="science.slug">
                    </div>
                </div>
                <div class="col">
                    <label for="sciences-cell-status margin-top">Problem status</label>
              <div id="sciences-cell-status">
                  <label for="is_solved">Is closed</label>
                  <input type="checkbox" id="is_solved" name="is_solved">
                </div>
                </div>
            </div>
    </div>
      <div class="row">
        <button class="btn btn-primary btn-large button">filter</button>
      </div>

    </div>
            <table style="background-color: white; margin-top: 100px; width:100%" border=1 frame=void>
                <tbody>
                <tr>
                    <td>Solved</td>
                    <td>Title</td>
                    <td>Solutions</td>
                    <td>Science</td>
                    <td>User</td>
                    <td>Time Asked</td>
                    <td>Time Answered</td>
                </tr>
                 <tr v-for="p in problems" v-bind:key="p">
                    <td v-if="p.is_closed">Yes</td>
                     <td v-else>No</td>
                    <td>{{ p.title }}</td>
                    <td>{{ p.title }}</td>
                    <td>{{ p.science.title }}</td>
                    <td>{{ p.user.username }}</td>
                    <td>{{ p.time_asked }}</td>
                    <td v-if="p.is_closed">{{ p.time_solved }}</td>
                    <td v-else>-</td>
                    <td>
                        <button>
                            <router-link :to="{name: 'problem', params: {problem_id: p.id}}">Go</router-link>
                        </button>
                    </td>
                </tr>
                </tbody>
            </table>
</template>


<style scoped>
@import '../../assets/css/problems.css';
</style>