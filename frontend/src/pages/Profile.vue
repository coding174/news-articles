<template>
  <div>
    <h1>Edit Profile</h1>
    <div v-if="userStore.user">
      <form @submit.prevent="updateProfile">
        <!-- Input fields for updating user information -->
        <label for="first_name">First Name:</label>
        <input v-model="userStore.user.first_name" type="text" id="first_name" required />

        <label for="last_name">Last Name:</label>
        <input v-model="userStore.user.last_name" type="text" id="last_name" required />

        <label for="email">Email:</label>
        <input v-model="userStore.user.email" type="email" id="email" required />

        <label for="birth_date">Birth Date:</label>
        <input v-model="userStore.user.birth_date" type="date" id="birth_date" required />

        <button type="submit">Update Profile</button>
      </form>
    </div>
    <div v-else>
      <p>User not found</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted} from 'vue';
import { useUserStore } from '../store/userStore.ts';

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const updateProfile = async () => {
      if(userStore.user != null){
        await userStore.updateUserInfo(userStore.user);
      }
    };

    // Fetch user information when the component is mounted
    onMounted(() => {
      userStore.fetchUserInfo();
    });

    return {
      userStore,
      updateProfile,
    };
  },
});
</script>
