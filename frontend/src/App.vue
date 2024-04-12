<script>
import Footer from "@/components/Footer.vue";
import {getUser, logoutUser} from "@/services/Auth";

export default {
  name: "AppItem",
  components: {
    Footer,
  },

  data() {
    return {
      publicPath: process.env.BASE_URL,
      githubUrl: 'https://github.com/michael7nightingale/FastAPI-Science',
      menuOpened: false
    }
  },

  computed: {
    user() {
      return getUser();
    }
  },

  methods: {
    logoutClick() {
      logoutUser()
      window.location.reload();
    },
    openMobileMenu() {
      this.menuOpened = !this.menuOpened;
    },
    checkLogin(){
      let user = getUser();
      if (!user){
        window.location = this.$router.resolve({name: "login"}).fullPath;
      }
    }
  },
  watch: {
    // eslint-disable-next-line no-unused-vars
    $route(to, from) {
      this.menuOpened = false;
      document.title = to.meta.title ? `${to.meta.title} | Сайт для вычислений` : 'Сайт для вычислений'
      const description = document.querySelector('meta[name="description"]')
      if (description) {
        description.setAttribute("content", to.meta.description ? `${to.meta.description} | Сайт для вычислений` : 'Сайт для вычислений')
      }
      let loginRequired = to.loginRequired || false;
      if (loginRequired){
        this.checkLogin();
      }
    }
  }


}

</script>


<template>
  <header class="bg-white shadow-lg">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1">
        <a href="/" class="-m-1.5 p-1.5">
          <span class="sr-only">Сайт для вычислений</span>
          <img class="h-8 w-auto" :src="'/images/logo.png'" alt="Логотип">
        </a>
      </div>
      <div class="flex lg:hidden">
        <button type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
                @click="openMobileMenu">
          <span class="sr-only">Open main menu</span>
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
               aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/>
          </svg>
        </button>
      </div>
      <div class="hidden lg:flex lg:gap-x-12">
        <router-link :to="{name: 'homepage'}" class="text-sm font-semibold leading-6 text-gray-900">
          Главная
        </router-link>
        <router-link :to="{name: 'about'}" class="text-sm font-semibold leading-6 text-gray-900">
          О портале
        </router-link>
        <router-link :to="{name: 'cabinet'}" class="text-sm font-semibold leading-6 text-gray-900" v-if="user">
          Кабинет
        </router-link>
        <a :href="githubUrl" target="_blank" class="text-sm font-semibold leading-6 text-gray-900">
          GitHub
        </a>
      </div>
      <div class="hidden lg:flex lg:flex-1 lg:justify-end">
        <a href="#" @click="logoutClick" class="text-sm font-semibold leading-6 text-gray-900" v-if="user">
          Выйти
          <span aria-hidden="true">&rarr;</span>
        </a>
        <router-link :to="{name: 'login'}" class="text-sm font-semibold leading-6 text-gray-900" v-else>
          Войти
          <span aria-hidden="true">&rarr;</span>
        </router-link>
      </div>
    </nav>
    <!-- Mobile menu, show/hide based on menu open state. -->
    <div class="lg:hidden" role="dialog" aria-modal="true" :style="menuOpened ? 'display: block' : 'display: none'"
         id="mobile-nav">
      <!-- Background backdrop, show/hide based on slide-over state. -->
      <div
          class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
        <div class="flex items-center justify-between">
          <a href="#" class="-m-1.5 p-1.5">
            <span class="sr-only">Your Company</span>
            <img class="h-8 w-auto" :src="'/images/logo.png'" alt="Логотип">
          </a>
          <button type="button" class="-m-2.5 rounded-md p-2.5 text-gray-700" @click="openMobileMenu">
            <span class="sr-only">Close menu</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                 aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10">
            <div class="space-y-2 py-6">
              <router-link :to="{name: 'homepage'}"
                           class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                Главная
              </router-link>
              <router-link :to="{name: 'about'}"
                           class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                О портале
              </router-link>
              <router-link :to="{name: 'cabinet'}" v-if="user"
                           class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                Кабинет
              </router-link>
              <a class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                 :href="githubUrl" target="_blank">
                GitHub
              </a>
            </div>
            <div class="py-6">
              <a href="#" @click="logoutClick" v-if="user"
                 class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                Выйти
              </a>
              <router-link :to="{name: 'login'}" v-else
                           class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                Войти
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main>
    <router-view/>
  </main>
  <Footer/>
</template>

<style>
@import './assets/css/global.css';
@import './assets/css/loader.css';
@import './assets/css/main.css';
@import './assets/css/output.css';
</style>
