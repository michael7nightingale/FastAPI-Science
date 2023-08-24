import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/main/HomeView.vue';
import AboutView from "@/views/main/AboutView.vue";
import LoginView from "@/views/users/LoginView.vue";
import RegisterView from "@/views/users/RegisterView.vue";
import SciencesListView from "@/views/sciences/SciencesListView.vue";
import ScienceDetailView from "@/views/sciences/ScienceDetailView.vue";
import CategoryDetailView from "@/views/sciences/CategoryDetailView.vue";
import PlotView from "@/views/sciences/PlotView.vue";
import FormulaDetailView from "@/views/sciences/FormulaDetailView.vue";
import CabinetView from "@/views/cabinets/CabinetView.vue";
import HistoryView from "@/views/cabinets/HistoryView.vue";
import ProblemsListView from "@/views/problems/ProblemsListView.vue";
import ProblemView from "@/views/problems/ProblemView.vue";
import ProblemCreateView from "@/views/problems/ProblemCreateView.vue";


const routes = [
  // main
  {
    path: '/',
    name: 'homepage',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },

  // auth
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

   // cabinets
  {
    path: '/cabinet',
    name: 'cabinet',
    component: CabinetView
  },
  {
    path: '/cabinet/history',
    name: 'cabinet/history',
    component: HistoryView

  },

   // sciences
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
    path: '/special-category/plots',
    name: 'plots',
    component: PlotView
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

   // problems
  {
    path: '/problems',
    name: 'problems',
    component: ProblemsListView
  },
  {
    path: '/problems/create',
    name: 'problem-create',
    component: ProblemCreateView
  },
  {
    path: '/problems/:problem_id',
    name: 'problem',
    component: ProblemView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
