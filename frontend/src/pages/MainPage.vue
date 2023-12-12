<template>
  <div>
    <h1>News Articles</h1>

    <!-- Navigation bar for categories -->
    <ul class="nav-bar">
      <li @click="filterCategory('All')">All</li>
      <li v-for="category in categories" :key="category.id" @click="filterCategory(category.id)">
        {{ category.name }}
      </li>
      <li v-if="user && user.favorite_categories && user.favorite_categories.length > 0"
        @click="filterCategory('Favorite')">
        Favorite Category
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
    <div v-else-if="selectedCategory === 'Favorite'">
      <div v-for="article in filteredArticles" :key="article.id">
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
  import { defineComponent, onMounted, computed } from "vue";
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
        user: computed(() => userStore.user as { favorite_categories?: { id: number }[] }),
      };
    },
    data() {
      return {
        articles: [] as Article[],
        categories: [] as Category[],
        selectedCategory: 'All',
        filteredArticles: [] as Article[],
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
            this.articles = data.articles;
            this.filteredArticles = this.articles;
          })
          .catch(error => {
            console.error('Error fetching articles:', error);
          });
      },
      fetchCategories() {
        fetch('http://localhost:8000/api/categories/')
          .then(response => response.json())
          .then(data => {
            this.categories = data.categories;
          })
          .catch(error => {
            console.error('Error fetching categories:', error);
          });
      },
      filterCategory(categoryId: string) {
        if (categoryId === 'All') {
          this.selectedCategory = 'All';
          this.filteredArticles = this.articles;
        } else if (categoryId === 'Favorite') {
          this.selectedCategory = 'Favorite';
          if (this.user && this.user.favorite_categories && this.user.favorite_categories.length > 0) {
            const favoriteCategoryIds = this.user.favorite_categories.map(cat => cat.id);
            this.filteredArticles = this.articles.filter(article => favoriteCategoryIds.includes(article.category_id));
          } else {
            this.filteredArticles = [];
          }
        } else {
          this.selectedCategory = categoryId;
          this.filteredArticles = this.articles.filter(article => article.category_id === parseInt(categoryId, 10));
        }
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