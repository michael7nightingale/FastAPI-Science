<script>
import {deleteHistory, getHistoryList} from "@/services/CabinetService";

export default {
  name: "HistoryView",
  data() {
    return {
        history: []
    }
  },

  computed: {
      User(){
        return JSON.parse(localStorage.userData);
      }
  },

  mounted() {
        getHistoryList()
            .then((response) => {
              this.history = response.data;
            })
  },
  methods: {
      deleteButtonClick(){
          deleteHistory()
              .then((response) => {
                console.log(response.data);
              })
      }
  }

}
</script>


<template>
<div class="jumbotron">
    <h2>Журнал вычислений</h2>
    <p class="lead">Скачать или удалить историю вычислений.</p>
    <router-link to="/cabinet" class="btn btn-primary btn-large">назад к кабинету &raquo;</router-link>
</div>

<div class="container">
  <div class="row">
    <div class="col">
      <label class="white_text" for="filename-input">Название файла</label>
    </div>
    <div class="col">
      <label class="white_text" for="extension-input">Extension</label>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <input class="white_text form-control" style="width: 30%" id='filename-input' type="text" name="filename" placeholder="Скачать как:">
    </div>
    <div class="col">
      <select class="form-control" style="width: 30%" id='extension-input' name="extension">
        <option value="csv">.csv</option>
        <option value="xls">.xls</option>
        <option value="xlsx">.xlsx</option>
        <option value="odt">.odt</option>
      </select>
    </div>
  </div>
  <div class="row">
    <button class="btn btn-large" style="background-color: dodgerblue" >Скачать</button>
  </div>
<table style="background-color: white; margin-top: 100px; width:100%" border=1 frame=void>
    <tbody >
        <tr>
            <td>Result</td>
            <td>Date Time</td>
            <td>Formula</td>
        </tr>
        <tr v-for="h in history" v-bind:key="h">
            <td>{{ h.result }}</td>
            <td>{{ h.date_time }}</td>
            <td>
                {{ h.formula_id }}
            </td>
        </tr>
    </tbody>
</table>
    <button class="btn-link" @click="deleteButtonClick">Удалить историю</button>
</div>
</template>


<style>

</style>