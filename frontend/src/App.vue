<template>
    <main class="container pt-4">
        <div class="navigation-links">
            <router-link class="nav-link" :to="{ name: 'Article' }">Articles</router-link>
            <span class="divider">|</span>
            <router-link class="nav-link" :to="{ name: 'Profile' }">Profile</router-link>
            <span class="divider">|</span>
            <router-link class="nav-link" :to="{ name: 'Logout' }">Logout</router-link>
        </div>
        <RouterView class="content-section" />
    </main>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { RouterView } from "vue-router";
    import MainPage from "./pages/MainPage.vue";

    export default defineComponent({
        components: { RouterView, MainPage },
    });


</script>

<style scoped>
    .navigation-links {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    .nav-link {
        text-decoration: none;
        color: #333;
        font-size: 18px;
        margin: 0 10px;
        transition: color 0.3s ease-in-out;
    }

    .nav-link:hover {
        color: #ff6b6b;
        /* Change color on hover */
    }

    .divider {
        margin: 0 5px;
        color: #999;
        font-size: 18px;
    }

    .content-section {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>