<template>
  <div>
    <h1>News Articles</h1>

    <!-- Navigation bar for categories -->
    <ul class="nav-bar">
      <li @click="filterCategory('All')">All</li>
      <li v-for="category in categories" :key="category.id" @click="filterCategory(category.id)">
        {{ category.name }}
      </li>
    </ul>

    <!-- Display filtered articles based on selected category -->
    <div v-if="selectedCategory === 'All'">
      <div v-for="article in articles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <hr />
      </div>
    </div>
    <div v-else>
      <div v-for="article in filteredArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <hr />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent,  onMounted, computed } from "vue";
  import { useUserStore } from "../store/userStore";
  import { Category, Article } from "../store/type.ts";

  export default defineComponent({
    setup() {
      const userStore = useUserStore();

      // Call fetchUserInfo when the component is mounted or when the user logs in
      onMounted(() => {
        userStore.fetchUserInfo();
      });

      return {
        user: computed(() => userStore.user),
      };
    },
    data() {
      return {
        articles: [] as Article[],
        categories: [] as Category[],
        selectedCategory: 'All',
        filteredArticles: [] as Article[], // Added a property to hold filtered articles
      };
    },
    mounted() {
      // Fetch articles and categories from Django backend and set the data
      this.fetchArticles();
      this.fetchCategories();
    },
    methods: {
      fetchArticles() {
        fetch('http://localhost:8000/api/articles/')
          .then(response => response.json())
          .then(data => {
            this.articles = data.articles; // Assuming your API response contains articles
            this.filteredArticles = this.articles; // Initialize filteredArticles with all articles
          })
          .catch(error => {
            console.error('Error fetching articles:', error);
          });
      },
      fetchCategories() {
        fetch('http://localhost:8000/api/categories/')
          .then(response => response.json())
          .then(data => {
            this.categories = data.categories; // Assuming your API response contains categories
          })
          .catch(error => {
            console.error('Error fetching categories:', error);
          });
      },
      filterCategory(categoryId : string) {
        console.log('Selected Category ID:', categoryId);
        if (categoryId === 'All') {
          this.selectedCategory = 'All';
          this.filteredArticles = this.articles; // Show all articles if 'All' is selected
        } else {
          this.selectedCategory = categoryId;
          this.filteredArticles = this.articles.filter(article => article.category_id === parseInt(categoryId, 10));
        }
        console.log('Selected Category:', this.selectedCategory);
        console.log('Filtered Articles:', this.filteredArticles);
      },
    },
  });
</script>

<style scoped>
  /* Styling for the category navigation bar */
  .nav-bar {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: center;
    background-color: #f2f2f2;
  }

  .nav-bar li {
    display: inline-block;
    padding: 10px 20px;
    cursor: pointer;
  }

  .nav-bar li:first-child {
    margin-left: 0;
    /* Remove left margin for the first navigation item */
  }

  .nav-bar li:hover {
    background-color: #ddd;
  }
</style>