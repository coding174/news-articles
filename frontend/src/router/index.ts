// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import Profile from '../pages/Profile.vue';
import Logout from '\../pages/Logout.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/articles/', name: 'Article', component: MainPage },
        { path: '/profile/', name: 'Profile', component: Profile },
        { path: '/logout/', name: 'Logout', component: Logout },
    ]
})

export default router
