<template>
    <main class="container pt-4">
        <div>
            <router-link
                class=""
                :to="{name: 'Article'}"
            >
                Articles
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Profile'}"
            >
                Profile
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Logout'}"
            >
                Logout
            </router-link>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import MainPage from "./pages/MainPage.vue";

export default defineComponent({
    components: { RouterView, MainPage},
});


</script>

<style scoped>
</style>
