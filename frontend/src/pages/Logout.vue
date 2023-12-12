<template>
  <div>
    <h1>Logging out...</h1>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted} from 'vue';
import { useUserStore } from '../store/userStore.ts';

export default defineComponent({
  setup() {
    const userStore = useUserStore();

    // Fetch user information when the component is mounted
    onMounted(() => {
      userStore.logout();
    });

    return {
      userStore,
    };
  },
});
</script>