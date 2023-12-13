<template>
    <div>
        <div v-if="userStore.user">
                <!-- Input fields for updating user information -->
                <label for="profile_image">Profile Picture:</label>
                <input type="file" id="profile_image" @change="handleFileUpload" />
                <div v-if="userStore.user.profile_image">
                    <img :src="getUserProfileImageUrl()" alt="Profile Picture" />
                </div>
        </div>
        <div v-else>
            <p>User not found</p>
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import { useUserStore } from '../store/userStore.ts';

export default defineComponent({
    setup() {
        const userStore = useUserStore();

        const getUserProfileImageUrl = (): string => {
            if (userStore.user && userStore.user.profile_image) {
                return `http://localhost:8000${userStore.user.profile_image}`;
            }
            return ''; // Return a default image URL if the profile picture is not available
        };

        const handleFileUpload = (event: Event) => {
            // Narrow down the type to HTMLInputElement
            const inputElement = event.target as HTMLInputElement;
            const formData = new FormData();

            // Check if the input element is indeed a file input
            if (inputElement.type === 'file') {
                const file = inputElement.files ? inputElement.files[0] : null;
                if (file) {
                    formData.append('profile_image', file);
                    userStore.setProfileImage(formData);
                }
            }
        };

        return {
            userStore,
            getUserProfileImageUrl,
            handleFileUpload,
        };
    },
});

</script>