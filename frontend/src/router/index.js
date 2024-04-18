import {createRouter, createWebHashHistory} from 'vue-router';
import HomeView from '@/views/main/HomeView.vue';
import LoginView from "@/views/users/LoginView.vue";
import RegisterView from "@/views/users/RegisterView.vue";
import SciencesListView from "@/views/sciences/SciencesListView.vue";
import ScienceDetailView from "@/views/sciences/ScienceDetailView.vue";
import CategoryDetailView from "@/views/sciences/CategoryDetailView.vue";
import PlotView from "@/views/sciences/PlotView.vue";
import FormulaDetailView from "@/views/sciences/FormulaDetailView.vue";
import CabinetView from "@/views/cabinets/CabinetView.vue";
import EquationsView from "@/views/sciences/EquationsView.vue";
import CallbackView from "@/views/users/CallbackView.vue";
import AboutView from "@/views/main/AboutView.vue";
import ActivationView from "@/views/users/ActivationView.vue";
import NotFound from "@/views/errors/NotFound.vue";


const routes = [
    // main
    {
        path: '/',
        name: 'homepage',
        component: HomeView,
        meta: {
            title: 'Главная',
            description: 'Главная'
        }
    },
    {
        path: '/about',
        name: 'about',
        component: AboutView,
        meta: {
            title: 'О портале',
            description: 'О портале'
        }
    },

    // auth
    {
        path: '/auth/login',
        name: 'login',
        component: LoginView,
        meta: {
            title: 'Вход в аккаунт',
            description: 'Вход в аккаунт'
        }
    },
    {
        path: '/auth/register',
        name: 'register',
        component: RegisterView,
        meta: {
            title: 'Регистрация аккаунта',
            description: 'Регистрация аккаунта'
        }
    },
    {
        path: '/auth/activation',
        name: 'activation',
        component: ActivationView,
        meta: {
            title: 'Активация аккаунта',
            description: 'Активация аккаунта'
        }
    },
    {
        path: '/auth/:providerName/callback',
        name: 'oauth_callback',
        component: CallbackView
    },

    // cabinets
    {
        path: '/cabinet',
        name: 'cabinet',
        component: CabinetView,
        loginRequired: true,
        meta: {
            title: 'Личный кабинет',
            description: 'Личный кабинет'
        },
    },

    // sciences
    {
        path: '/sciences',
        name: 'sciences',
        component: SciencesListView,
    },
    {
        path: '/science/:slug',
        name: 'science',
        component: ScienceDetailView
    },
    {
        path: '/special-category/plots',
        name: 'plots',
        component: PlotView,
        meta: {
            title: 'Графики',
            description: 'Графики'
        },
        loginRequired: true,
    },
    {
        path: '/special-category/equations',
        name: 'equations',
        component: EquationsView,
        meta: {
            title: 'Уравнения',
            description: 'Уравнения'
        },
        loginRequired: true,
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
    // {
    //     path: '/problems',
    //     name: 'problems',
    //     component: ProblemsListView,
    // },
    // {
    //     path: '/problems/create',
    //     name: 'problem-create',
    //     component: ProblemCreateView
    // },
    // {
    //     path: '/problems/:problem_id',
    //     name: 'problem',
    //     component: ProblemView
    // },

    // errors
    {
        path: "/404",
        name: 'not-found',
        component: NotFound
    },
    {
        path: "/:catchAll(.*)",
        redirect: "/404",
    },

]

const router = createRouter({
    history: createWebHashHistory(process.env.BASE_URL),
    routes
})

export default router
