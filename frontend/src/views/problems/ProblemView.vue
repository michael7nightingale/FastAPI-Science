<script>
export default {
  name: "ProblemView",
  data(){
    return {
      problem: {},
      solutions: [],

    }
  },


}
</script>


<template>
 <div class="jumbotron">
         <h2>{{ problem.title }}</h2>
         <p class="lead">Time asked: {{ problem.time_asked }}</p>
         {% if problem.time_solved %}
         <p class="lead">Status: solved ({{ problem.time_solved }})</p>
         {% else %}
         <p class="lead">Status: opened</p>
         {% endif %}
         <div class="row">
             <div class="col-2">
                 <a href="{{ url_for('problems_all') }}" class="btn btn-primary btn-large">back to problems &raquo;</a>
             </div>
             <div class="col-2">
             </div>
        </div>
    </div>



<div class="container problem">
<div class="tabs">
  <input type="radio" name="tab-btn" id="tab-btn-1" value="" checked>
  <label for="tab-btn-1">Problem</label>
  <input type="radio" name="tab-btn" id="tab-btn-2" value="">
  <label for="tab-btn-2">Media</label>
    <input type="radio" name="tab-btn" id="tab-btn-3" value="">
  <label for="tab-btn-3">Solutions</label>
    <input type="radio" name="tab-btn" id="tab-btn-4" value="">
  <label for="tab-btn-4">My solutions</label>
  <input type="radio" name="tab-btn" id="tab-btn-5" value="">
  <label for="tab-btn-5">Create solution</label>


  <div id="content-1">
        <h5 align="center">Content</h5>
          <p>{{ problem.text }}</p>
  </div>


  <div id="content-2">
<!--                <ul >-->
<!--                    <li>-->
                        <img src="{{ url_for('static', path=m.media_path) }}" alt="" width="100%">
<!--                    </li>-->
<!--                </ul>-->
<!--                <p>There is no media supplied</p>-->
  </div>


     <div id="content-3">
          <div class="solution" v-for="s in solutions" v-bind:key="s">
        <p>{{ s.text }}</p>
                <ul v-if="s">
<!--{#                    <li>#}-->
<!--{#                        <img backend="{{ url_for('static', path=m.media_path) }}" alt="" width="100%">#}-->
<!--{#                    </li>#}-->
                </ul>
                <p v-else>There is no media supplied</p>
          </div>

  </div>


    <div id="content-4">
         <div class="container" style="border-radius: 10px">
         </div>
  </div>


  <div id="content-5">
            <div class="row">
                <div class="col">
                    <label for="text" class="white_text">Text</label>
                    <textarea class="form-control" placeholder="Text" name="text" id="text"></textarea>
                </div>

            </div>
           <button type="button" class="btn btn-primary btn-large margin-top margin-bottom" onclick="addMedia(event)">+Add media</button>
          <div id="medias">
              <div class="row">
              <div class="col">
                  <input class="form-control" type="file" name="media1" id="input-media-1">
              </div>
                  <button class="delete-button" id="button-delete-1" onclick="deleteMedia(event)">Delete</button>
              </div>
           </div>
            <div class="row">
                <button class="btn btn-primary btn-large margin-top margin-bottom">Create</button>
            </div>
  </div>
</div>

</div>
</template>


<style scoped>
@import '../../assets/css/problems.css';
</style>