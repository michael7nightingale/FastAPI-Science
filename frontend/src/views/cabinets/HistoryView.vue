<script>
import {deleteHistory, downloadHistory, getHistoryList} from "@/services/CabinetService";
import {getUser} from "@/services/Auth";

export default {
  name: "HistoryView",
  data() {
    return {
        history: [],
        extension: "csv",
        filename: "history"
    }
  },

  computed: {
      User(){
        return JSON.parse(localStorage.userData);
      }
  },

  mounted() {
    let user = getUser();
    if (!user){
      window.location = this.$router.resolve({name: "login"}).fullPath;
    }
    getHistoryList()
        .then((response) => {
          this.history = response.data;
        })
  },
  methods: {
      deleteButtonClick(){
          deleteHistory()
              .then((response) => {
                response
                this.history = []
              })
      },

      downloadClick(){
        downloadHistory(this.filename, this.extension)
            .then((response) => {
                const blob = new Blob([response.data], { type: `application/${this.extension}` });
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = `${this.filename}.${this.extension}`;
                link.click();
                URL.revokeObjectURL(link.href);
            })
      }
  },

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
      <label for="filename-input">Название файла</label>
    </div>
    <div class="col">
      <label for="extension-input">Расширение файла</label>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <input class="form-control" type="text" :value="filename" @input="($event) => filename = $event.target.value" placeholder="Скачать как:">
    </div>
    <div class="col">
      <select class="form-control" id='extension-input' v-model="extension" name="extension">
        <option value="csv">.csv</option>
        <option value="xls">.xls</option>
        <option value="xlsx">.xlsx</option>
        <option value="odt">.odt</option>
      </select>
    </div>
  </div>
  <div class="row">
    <div class="col">
       <button class="btn btn-large button-blue" @click="downloadClick">Скачать</button>
  </div>
    </div>

<table style="background-color: white; margin-top: 100px; width:100%" border=1 frame=void>
    <tbody >
        <tr>
            <td>Результат</td>
            <td>Время</td>
            <td>Формула</td>
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
  <button class="btn btn-large button-red" @click="deleteButtonClick">Удалить историю</button>
</div>
</template>


<style>
</style>