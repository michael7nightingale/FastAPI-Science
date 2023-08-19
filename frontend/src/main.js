import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueMathjax from 'vue-mathjax'


createApp(App).use(router).use(VueMathjax).mount('#app')
