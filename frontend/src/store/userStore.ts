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
    profileImage: null as File | null,
  }),
  actions: {

    async setProfileImage(formData: FormData) {
      formData.forEach((value, key) => {
          console.log(`${key}: ${value}`);
      });

      try {
        const response = await fetch('http://localhost:8000/api/imageUpdate/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'X-CSRFToken': getCsrfToken(), 
          },
          body: formData,
        });

        if (response.status === 200) {
          console.log('User image updated successfully');
          await this.fetchUserInfo();
        } 
      } 
      catch (error) {
        console.error('Error updating user image:', error);
      }
    },
    
    async fetchUserInfo() {
      try {
        const response = await fetch('http://localhost:8000/api/editPersonData/', {
          method: 'GET',
          credentials: 'include'
        });

        const userData = await response.json();
        this.setUser(userData.person);
      } 
      catch (error) {
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
            'X-CSRFToken': getCsrfToken(),
          },
          body: JSON.stringify(user),
        });

        if (response.ok) {
          console.log('User information updated successfully');
          await this.fetchUserInfo();
        }
      } 
      catch (error) {
        console.error('Error updating user information:', error);
      }
    },

    setUser(user: User) {
      this.user = user;
    },

    clearUser() {
      this.user = null;
    },

    async logout() {
      try {
        const response = await fetch('http://localhost:8000/logout/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
          },
        });

        if (response.ok) {
          console.log('User logged out successfully');
          this.clearUser();
          window.location.href = '/'; 
        }
      } catch (error) {
        console.error('Error logging out:', error);
      }
    }
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