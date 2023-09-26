<script>
import {getOauthProviderUrl} from "@/services/UserService";

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

  mounted() {

    let query = this.$route.params;
    console.log(123, query);

    for (let idx in this.providers){
      let newProxy = this.providers;
      let providerData = newProxy[idx];
      getOauthProviderUrl(providerData.name).
          then((response) => {
            providerData.url = response.data;
      })
      this.providers = newProxy;
    }
  },

}


</script>


<template>
 <a v-for="provider in providers" v-bind:key="provider" :href="provider.url">
     <img :src="provider.imageUrl" :alt="provider.name" style="width: 40px">
</a>
</template>


<style>

</style>