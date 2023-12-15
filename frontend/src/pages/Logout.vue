<script lang="ts">
  import { defineComponent, onMounted } from 'vue';
  import { useUserStore } from '../store/userStore.ts';

  export default defineComponent({
    setup() {
      const userStore = useUserStore();

      onMounted(() => {
        userStore.logout();
      });

      return {
        userStore,
      };
    },
  });
</script>