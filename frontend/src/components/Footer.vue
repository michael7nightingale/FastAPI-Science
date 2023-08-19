<script>
  export default {
    name: "FooterItem",
    data(){
      return{
        author: "michael7nightingale",
      }
    },
    computed:{
      year() {
        let now = new Date();
        return now.getFullYear();
      }
    }
  }
</script>

<template>
<footer class="footer_">
      <p class="">© {{ year }}, Все права защищены. Создан {{ author }}</p>
  </footer>
</template>

<style>

</style>