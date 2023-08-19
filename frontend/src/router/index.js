import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/main/HomeView.vue';
import AboutView from "@/views/main/AboutView.vue";
import LoginView from "@/views/users/LoginView.vue";
import RegisterView from "@/views/users/RegisterView.vue";
import SciencesListView from "@/views/sciences/SciencesListView.vue";
import ScienceDetailView from "@/views/sciences/ScienceDetailView.vue";
import CategoryDetailView from "@/views/sciences/CategoryDetailView.vue";
import FormulaDetailView from "@/views/sciences/FormulaDetailView.vue";


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },


  {
    path: '/auth/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/auth/register',
    name: 'register',
    component: RegisterView
  },


  {
    path: '/sciences',
    name: 'sciences',
    component: SciencesListView
  },
   {
    path: '/science/:slug',
    name: 'science',
    component: ScienceDetailView
  },
  {
    path: '/category/:slug',
    name: 'category',
    component: CategoryDetailView
  },
  {
    path: '/formula/:slug',
    name: 'formula',
    component: FormulaDetailView
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
