<script>
import {loginUser} from "@/services/UserService";
import {setUser} from "@/services/Auth";
import OAuth from "@/components/OAuth.vue";

export default {
  name: "LoginView",
  components: {OAuth},
  data(){
    return{
      loginMinLength: 6,
      passwordMinLength: 6,
      login: "",
      loginError: "",
      password: "",
      passwordError: "",

    }
  },
  methods: {
    loginClick(){
        let data;
        let wereError = false;
        if (this.login.length < this.loginMinLength) {
          wereError = true;
          this.loginError = `Логин должен содержать от ${this.loginMinLength} символов`
        }
        if (this.password.length < this.passwordMinLength) {
          wereError = true;
          this.passwordError = `Пароль должно содержать от ${this.passwordMinLength} символов`
        }
        if (wereError) return;
        loginUser(this.login, this.password)
            .then((response) => {
              data = response.data;
              setUser(data.access_token)
                  .then(() => {
                    window.location = this.$router.resolve({name: "homepage"}).fullPath;
                  });
            })
            .catch((error) => {
              this.errorText = error.response.data.detail;
            })
    },

    loginInput(value){
      this.login = value;
      if (this.login.length >= this.loginMinLength) this.loginError = "";
    },
    passwordInput(value){
      this.password = value;
      if (this.password.length >= this.passwordMinLength) this.passwordError = "";
    }
  }

}

</script>

<template>
<div class="container login-container">
  <h3 align="center">Вкод в аккаунт</h3>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Логин</label>
      <input type="text" placeholder="Логин:" :value="login" @input="loginInput($event.target.value)" class="form-style" autocomplete="off"/>
      <p class="text-danger" style="margin: 10px">{{ loginError }}</p>
    </div>
    <div class="form-item">
      <label class="form-label" for="form2Example2">Пароль</label>
      <input type="password" placeholder="Пароль:" :value="password" @input="passwordInput($event.target.value)" id="password" class="form-style" />
      <p class="text-danger" style="margin: 10px">{{ passwordError }}</p>
    </div>
    <div class="form-item">
        <router-link to="/auth/register" class="pull-left"><small>регистрация</small></router-link>
        <router-link to="/auth/register" class="pull-left margin-pull-left"><small>зыбыли пароль?</small></router-link>
        <button class="btn login pull-right" @click="loginClick" style="background-color: #fff; border:1px solid #55b1df; color:#55b1df; cursor:pointer;">
        Войти
      </button>
        <div class="clear-fix"></div>
    </div>
    <OAuth/>
</div>
</template>

<style>
</style>