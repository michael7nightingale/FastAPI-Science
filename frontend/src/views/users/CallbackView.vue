<script>
import {getOauthCallbackToken} from "@/services/UserService";
import {setUser} from "@/services/Auth";

export default {
  name: "CallbackView",
  mounted() {
    let query = this.$route.query;
    let code = query.code;
    if (code){
      getOauthCallbackToken(this.$route.params.providerName, code)
          .then((response) => {

            let data = response.data;
            setUser(data.access_token)
            window.location = this.$router.resolve({name: "homepage"}).fullPath;
          })

    .catch((error) => {
        alert(error.response.data.detail);
        window.location = this.$router.resolve({name: "login"}).fullPath;
      });
    }


  }
}
</script>

<template>
<h3 class="base-title white_text">Callback data is received, please wait for redirect...</h3>
</template>

<style scoped>
.base-title{
  text-align: center;
}

</style>