import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../components/mainPage.vue'

const routes = 
[
	{
		path: '/',
		name: 'mainPage',
		component: mainPage
	}
]

const router = createRouter({
history: createWebHistory(process.env.BASE_URL),
routes
})

export default router
