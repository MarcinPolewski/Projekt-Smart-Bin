import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const g_endpoint = "http://localhost:8000/api/";

createApp(App).provide('g_endpoint', g_endpoint).use(router).mount('#app')
