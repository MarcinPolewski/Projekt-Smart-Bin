import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../components/mainPage.vue'
import fillingLevelPage from '../components/fillingLevelPage.vue'
import punctationPage from '../components/punctationPage.vue'
import userAddingPage from '../components/userAddingPage.vue'
import userAssignmentPage from '../components/userAssignmentPage.vue'

const routes = 
[
	{
		path: '/',
		name: 'mainPage',
		component: mainPage
	},
	{
		path: '/filling-level',
		name: 'fillingLevelPage',
		component: fillingLevelPage
	},
	{
		path: '/punctation',
		name: 'punctationPage',
		component: punctationPage
	},
	{
		path: '/add-user',
		name: 'userAddingPage',
		component: userAddingPage
	},
	{
		path: '/assign-user',
		name: 'userAssignmentPage',
		component: userAssignmentPage
	},
]

const router = createRouter({
history: createWebHistory(process.env.BASE_URL),
routes
})

export default router
