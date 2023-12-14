<template>
    <div>
        <h1>Edit Profile</h1>
        <div v-if="userStore.user">
            <form @submit.prevent="updateProfile">
                <ImageUpload /><br>

                <label for="first_name">First Name:</label>
                <input v-model="userStore.user.first_name" type="text" id="first_name" required /><br>

                <label for="last_name">Last Name:</label>
                <input v-model="userStore.user.last_name" type="text" id="last_name" required /><br>

                <label for="email">Email:</label>
                <input v-model="userStore.user.email" type="email" id="email" required /><br>

                <label for="birth_date">Birth Date:</label>
                <input v-model="userStore.user.birth_date" type="date" id="birth_date" required /><br>

                <label>Select Favorite Categories:</label>
                <div v-if="categories.length > 0">
                    <div v-for="category in categories" :key="category.id">
                        <input type="checkbox" :id="`category_${category.id}`" :value="category.id"
                            v-model="selectedCategories" />
                        <label :for="`category_${category.id}`">{{ category.name }}</label>
                    </div>
                </div>

                <div v-else>
                    <p>No categories available</p>
                </div>

                <div v-if="userData && userData.favorite_categories && userData.favorite_categories.length > 0">
                    <p>Your Favorite Categories:</p>
                    <ul>
                        <li v-for="favCategoryId in userData.favorite_categories" :key="favCategoryId">
                            {{ getCategoryName(favCategoryId) }}
                        </li>
                    </ul>
                </div>

                <button type="submit">Update Profile</button>
                <p v-if="isUpdateSuccessful" style="color: green;">Profile Updated Successfully!</p>
            </form>
        </div>
        <div v-else>
            <p>User not found</p>
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent, onMounted, ref, watchEffect } from 'vue';
    import { useUserStore } from '../store/userStore.ts';
    import ImageUpload from './ImageUpload.vue';

    interface Category {
        id: number;
        name: string;
    }

    export default defineComponent({
    setup() {
        const userStore = useUserStore();
        const userData = ref<any>(null);
        const selectedCategories = ref<number[]>([]);
        const categories = ref<Category[]>([]);
        const isUpdateSuccessful = ref(false);
        watchEffect(() => {
            console.log('Selected Categories:', selectedCategories.value);
        });
        const getCategoryName = (categoryId: number): string => {
            const foundCategory = categories.value.find(category => category.id === categoryId);
            return foundCategory ? foundCategory.name : '';
        };
        const updateProfile = async () => {
            if (userStore.user !== null) {
                try {
                    const user = {
                        id: userStore.user.id,
                        first_name: userStore.user.first_name,
                        last_name: userStore.user.last_name,
                        email: userStore.user.email,
                        birth_date: userStore.user.birth_date,
                        profile_image: userStore.user.profile_image,
                        favorite_categories: selectedCategories.value,
                    };
                    await userStore.updateUserInfo(user);
                    isUpdateSuccessful.value = true;
                    console.log(user)
                }
                catch (error) {
                    console.error('Error updating profile:', error);
                    isUpdateSuccessful.value = false;
                }
            }
        };
        onMounted(async () => {
            await fetchCategories();
            await fetchUserFavoriteCategories();
        });
        const fetchCategories = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/categories/', {
                    method: 'GET',
                });
                const data = await response.json();
                if (Array.isArray(data.categories)) {
                    categories.value = data.categories;
                }
            }
            catch (error) {
                console.error('Error fetching categories:', error);
            }
        };
        const fetchUserFavoriteCategories = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/editPersonData/', {
                    method: 'GET',
                });
                const fetchedData = await response.json();
                if (fetchedData.person && fetchedData.person.favorite_categories) {
                    userData.value = fetchedData.user; // Assign fetched user data to userData
                    selectedCategories.value = fetchedData.person.favorite_categories.map((category: {
                        id: number;
                    }) => category.id); // Store only category IDs
                }
            }
            catch (error) {
                console.error('Error fetching user favorite categories:', error);
            }
        };
        return {
            userStore,
            userData,
            selectedCategories,
            categories,
            updateProfile,
            isUpdateSuccessful,
            getCategoryName,
        };
    },
    components: { ImageUpload }
});
</script>