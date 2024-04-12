import { createApp, h } from 'vue'
import App from './App.vue'
import router from './router'


// createApp(App).use(VueMathjax).use(router).use(VueMathjax).mount('#app')

const app  = createApp({
    render: ()=>h(App)
});
app.use(router)
app.mount("#app")
