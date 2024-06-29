import { createWebHistory, createRouter } from "vue-router";

import LoginView from "./components/LoginView.vue";
import RegistrationView from "./components/RegistrationView.vue";
import Dashboard from "./components/Dashboard.vue";
import isAuthenticated from "./auth";

const routes = [
    {
        path: '/',
        component: RegistrationView
    },
    {
        path: '/register',
        component: RegistrationView
    },
    {
        path: '/sign-in',
        component: LoginView
    },
    {
        path: '/dashboard',
        component: Dashboard,
        meta: {requiredAuth: true}
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(async (to, from, next) => {
    if (to.matched.some(record => record.meta.requiredAuth)) {
        const authStatus = await isAuthenticated();
        if (!authStatus){
            next('/login');
        }
        else{
            next();
        }
    }
    else {
        next();
    }
});

export default router