import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import router from './router.js'

import 'primevue/resources/themes/lara-light-indigo/theme.css'
import 'primeflex/primeflex.css'

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import FloatLabel from 'primevue/floatlabel';
import Password from 'primevue/password';
import Dropdown from 'primevue/dropdown';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';


const app = createApp(App)
app.use(PrimeVue)
app.use(router)
app.use(ToastService)

app.component('Button', Button)
app.component("InputText", InputText)
app.component("FloatLabel", FloatLabel)
app.component("Password", Password)
app.component("Dropdown", Dropdown)
app.component("Toast", Toast)
app.mount('#app')
