<template>
    <div>
        <div v-if="userStore.user">
                <div v-if="userStore.user.profile_image" class="profile-image-container">
                    <img :src="userImagePath()" alt="Profile Picture" class="profile_image"/>
                </div>
                <input type="file" id="profile_image" @change="imageUpdate" />
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import { useUserStore } from '../store/userStore.ts';

    export default defineComponent({
        setup() {
            // Uses pinia store management
            const userStore = useUserStore();

            // Gets the profile image of the user to display it
            const userImagePath = (): string => {
                if (userStore.user && userStore.user.profile_image) {
                    return `http://localhost:8000${userStore.user.profile_image}`;
                }
                return '';
            };

            // Handles the file upload event and sets the profile image of the user
            const imageUpdate = (event: Event) => {
                const input = event.target as HTMLInputElement;
                const formData = new FormData();

                if (input.type === 'file') {
                    const file = input.files ? input.files[0] : null;
                    if (file) {
                        formData.append('profile_image', file);
                        userStore.setProfileImage(formData);
                    }
                }
            };

            return {
                userStore,
                userImagePath,
                imageUpdate,
            };
        },
    });
</script>

<style>
    .profile-image-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    }

    .profile_image {
    border-radius: 50%; 
    max-width: 190px; 
    max-height: 190px;
    width: 100%;
    height: auto; 
    display: block;
    margin: 0 auto; 
    }
</style>