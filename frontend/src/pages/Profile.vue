<template>
    <div class="edit-profile-container">
        <h1 class="edit-profile-title">Edit Profile</h1>
        <div v-if="userStore.user" class="edit-profile-form">
            <form @submit.prevent="updateProfile" class="form-container">
                <ImageUpload /><br>

                <div class="form-group">
                    <label for="first_name" class="form-label">First Name:</label>
                    <input v-model="userStore.user.first_name" type="text" id="first_name" required
                        class="form-input" />
                </div>

                <div class="form-group">
                    <label for="last_name" class="form-label">Last Name:</label>
                    <input v-model="userStore.user.last_name" type="text" id="last_name" required class="form-input" />
                </div>

                <div class="form-group">
                    <label for="email" class="form-label">Email:</label>
                    <input v-model="userStore.user.email" type="email" id="email" required class="form-input" />
                </div>

                <div class="form-group">
                    <label for="birth_date" class="form-label">Birth Date:</label>
                    <input v-model="userStore.user.birth_date" type="date" id="birth_date" required
                        class="form-input" />
                </div>

                <label class="form-label">Select Favorite Categories:</label>
                <div v-if="categories.length > 0" class="category-container">
                    <div v-for="category in categories" :key="category.id" class="category-item">
                        <input type="checkbox" :id="`category_${category.id}`" :value="category.id"
                            v-model="selectedCategories" />
                        <label :for="`category_${category.id}`" class="category-label">{{ category.name }}</label>
                    </div>
                </div>

                <div v-else>
                    <p class="no-categories">No categories available</p>
                </div>

                <div v-if="userData && userData.favorite_categories && userData.favorite_categories.length > 0"
                    class="favorite-categories">
                    <p>Your Favorite Categories:</p>
                    <ul>
                        <li v-for="favCategoryId in userData.favorite_categories" :key="favCategoryId"
                            class="fav-category-item">
                            {{ getCategoryName(favCategoryId) }}
                        </li>
                    </ul>
                </div>

                <button type="submit" class="submit-button">Update Profile</button>
                <p v-if="isUpdateSuccessful" class="success-message">Profile Updated Successfully!</p>
            </form>
        </div>
        <div v-else>
            <p class="user-not-found">User not found</p>
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
            const userData = ref < any > (null);
            const selectedCategories = ref < number[] > ([]);
            const categories = ref < Category[] > ([]);
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

<style scoped>
    .edit-profile-container {
      font-family: Arial, sans-serif;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f7f7f7;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
  
    .edit-profile-title {
      text-align: center;
      font-size: 24px;
      margin-bottom: 20px;
    }
  
    .edit-profile-form {
      margin-bottom: 20px;
    }
  
    .form-container {
      display: grid;
      grid-gap: 10px;
    }
  
    .form-group {
      display: flex;
      flex-direction: column;
    }
  
    .form-label {
      margin-bottom: 5px;
      font-weight: bold;
    }
  
    .form-input {
      padding: 8px;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 16px;
    }
  
    .category-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      grid-gap: 5px;
    }
  
    .category-item {
      display: flex;
      align-items: center;
    }
  
    .category-label {
      margin-left: 5px;
    }
  
    .no-categories {
      color: red;
    }
  
    .favorite-categories {
      margin-top: 10px;
    }
  
    .fav-category-item {
      margin-left: 20px;
      list-style: none;
    }
  
    .submit-button {
      padding: 10px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 18px;
      margin-top: 10px;
    }
  
    .success-message {
      color: green;
      margin-top: 10px;
    }
  
    .user-not-found {
      color: red;
    }
  </style>