import { createWebHistory, createRouter } from "vue-router";

import LoginView from "./components/LoginView.vue";
import RegistrationView from "./components/RegistrationView.vue";

const routes = [
    {
        path: '/',
        component: RegistrationView
    },
    {
        path: '/sign-in',
        component: LoginView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router