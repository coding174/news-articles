import { defineStore } from 'pinia';

interface User {
  first_name: '',
  last_name: '',
  email: '',
  birth_date: '',
  profile_image: '',
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
  }),
  actions: {
    async fetchUserInfo() {
      try {
        // Replace 'API_ENDPOINT' with your actual API endpoint
        const response = await fetch('http://localhost:8000/api/editPersonData/', {
          method: 'GET',
          credentials: 'include'
        });

        const userData = await response.json();
        this.setUser(userData.person);
      } catch (error) {
        console.error('Error fetching user information:', error);
      }
    },

    async updateUserInfo(user: User) {
      try {
        const response = await fetch('http://localhost:8000/api/editPersonData/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // Include the CSRF token in the headers
          },
          body: JSON.stringify(user),
        });

        if (response.ok) {
          console.log('User information updated successfully');

          // Fetch and update user information in the store
          await this.fetchUserInfo();
        } else {
          console.error('Error updating user information:', response.statusText);
        }
      } catch (error) {
        console.error('Error updating user information:', error);
      }
    },

    setUser(user: User) {
      this.user = user;
    },

    clearUser() {
      this.user = null;
    },
  },
});

const getCsrfToken = () => {
  const csrfCookieName = 'csrftoken'; // Adjust with your CSRF token cookie name
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${csrfCookieName}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || '';
  }
  return '';
};