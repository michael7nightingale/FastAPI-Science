<script>
export default {
  name: "OAuth",
  data(){
    return {
      providers: [
        {
          "name": "google",
          "imageUrl": "../images/google.png",
        },
        {
          "name": "github",
          "imageUrl": "../images/github.png",
        },
      ]
    }
  },

  methods:{

  },

}


</script>


<template>
 <a v-for="provider in providers" v-bind:key="provider">
     <img :src="provider.imageUrl" :alt="provider.name" style="width: 40px">
</a>
</template>


<style>

</style>