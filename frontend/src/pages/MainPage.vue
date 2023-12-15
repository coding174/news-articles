/**
* Template for the main news page.
*
* Displays a list of news articles filtered by selected category.
* Allows submitting and managing comments on each article.
*/

<template>
  <div class="news-container">
    <h1 class="news-header">Discover Latest News</h1>

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
    <div v-for="article in filteredArticles" :key="article.id" class="article">
      <h2 class="article-title">{{ article.title }}</h2>
      <p class="article-content">{{ article.content }}</p>
      <hr class="article-divider" />
      <!-- Place the comment form after each article -->
      <form @submit.prevent="submitComment(getArticleId(article))" class="comment-form">
        <textarea v-model="articleComments[article.id]" placeholder="Type your comment here"
          class="comment-textarea"></textarea>
        <button type="submit" class="comment-submit-btn">Submit Comment</button>
      </form>
      <!-- comments -->
      <ul class="comment-list">
        <li v-for="comment in article.comments" :key="comment.id" class="comment">
          <div v-if="!comment.editing" class="comment-content">
            <span>{{ comment.content }}</span>
            <div v-if="showButtons(comment)" class="comment-buttons">
              <button @click="editComment(comment)" class="comment-btn">Edit</button>
              <button @click="deleteComment(article, comment)" class="comment-btn">Delete</button>
            </div>
          </div>
          <div v-else class="comment-edit">
            <textarea v-model="comment.updatedContent" placeholder="Edit your comment"
              class="comment-edit-textarea"></textarea>
            <button @click="saveEditedComment(article, comment)" class="comment-edit-save-btn">Save</button>
            <button @click="cancelEdit(comment)" class="comment-edit-cancel-btn">Cancel</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, onMounted, computed, ref } from "vue";
  import { useUserStore, getCsrfToken } from "../store/userStore";
  import { Category, Article, Comment } from "../store/type.ts";

  interface ArticleComments {
    [key: string]: string;
  }

  export default defineComponent({
    setup() {
      const userStore = useUserStore();
      const userID = ref < number | undefined > (userStore.user?.id);
      // Call fetchUserInfo when the component is mounted or when the user logs in
      onMounted(async () => {
        console.log("Component mounted");

        try {
          await userStore.fetchUserInfo();
          userID.value = userStore.user?.id;
          console.log("User ID:", userID.value);
        } catch (error) {
          console.error('Error fetching user info:', error);
        }
      });

      return {
        userID,
        user: computed(() => userStore.user as { favorite_categories?: { id: number }[] }),
        comments: [] as Comment[], // Declare comments property
        filteredComments: [] as Comment[],
        selectedArticleId: '',
      };
    },
    data() {
      return {
        articles: [] as Article[],
        categories: [] as Category[],
        selectedCategory: 'All',
        filteredArticles: [] as Article[],
        newComment: '',
        articleComments: {} as ArticleComments,
      };
    },
    mounted() {
      console.log("Component2 mounted");
      // Fetch articles and categories from Django backend and set the data
      this.fetchArticles();
      this.fetchCategories();
    },
    methods: {
      showButtons(comment: Comment) {
        return this.userID === Reflect.get(comment, 'user_id') || this.userID === Reflect.get(comment, 'userId');
      },

      editComment(comment: Comment) {
        console.log("HELL:LLL", this.userID, Reflect.get(comment, 'user_id'))
        console.log(comment)
        if (this.userID === Reflect.get(comment, 'user_id') || this.userID === Reflect.get(comment, 'userId')) {
          comment.editing = true;
          comment.updatedContent = comment.content;
        }
      },
      cancelEdit(comment: Comment) {
        comment.editing = false;
      },
      saveEditedComment(article: Article, comment: Comment) {
        if (comment.updatedContent !== undefined && comment.updatedContent.trim() !== '') {
          console.log("Saving edited comment:", comment.updatedContent, comment);

          const updateCommentApi = `http://localhost:8000/api/edit_comment/${comment.id}/`;

          fetch(updateCommentApi, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
              content: comment.updatedContent,
            }),
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(updatedComment => {
              console.log('Updated comment:', updatedComment);
              // Update the local comment content after the API call succeeds
              console.log("c", article.comments);
              console.log("comment", comment.id);
              const updatedCommentIndex = article.comments.findIndex(c => c.id === comment.id);
              console.log("updatedCommentIndex:", updatedCommentIndex);
              if (updatedCommentIndex !== -1) {
                article.comments[updatedCommentIndex].content = String(comment.updatedContent);
                article.comments[updatedCommentIndex].editing = false;
              }
              console.log(article.comments[updatedCommentIndex].content)
            }
            )
            .catch(error => {
              console.error('Error updating comment:', error);
            });
        } else {
          console.error('Empty comment. Cannot update.');
        }
      },

      deleteComment(article: Article, comment: Comment) {
        if (this.userID === Reflect.get(comment, 'user_id') || this.userID === Reflect.get(comment, 'userId')) {
          console.log("Deleting comment:", comment.id);
          // Perform API call to delete the comment
          fetch(`http://localhost:8000/api/delete_comment/${comment.id}/`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
              'X-CSRFToken': getCsrfToken(),
            },
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              // Remove the comment from the UI after successful deletion
              const commentIndex = article.comments.findIndex(c => c.id === comment.id);
              if (commentIndex !== -1) {
                article.comments.splice(commentIndex, 1);
              }
            })
            .catch(error => {
              console.error('Error deleting comment:', error);
            });
        }
      },

      getArticleId(article: Article): number {
        return typeof article.id === 'string' ? parseInt(article.id, 10) : article.id;
      },

      submitComment(articleId: number) {
        console.log("Submitting comment for article:", articleId);
        if (this.articleComments[articleId] && this.articleComments[articleId].trim() !== '') {
          this.postComment(articleId, this.articleComments[articleId]);
          this.articleComments[articleId] = '';
        } else {
          console.error('Empty comment. Cannot post a comment.');
        }
      },
      fetchArticles() {
        fetch('http://localhost:8000/api/articles/')
          .then(response => response.json())
          .then(data => {
            this.articles = data.articles;
            this.filteredArticles = this.articles;

            // Fetch comments for each article
            this.articles.forEach(article => {
              const articleId = typeof article.id === 'string' ? parseInt(article.id, 10) : article.id;

              if (typeof articleId === 'number' && !isNaN(articleId)) {
                this.fetchComments(articleId).then((comments: Comment[]) => {
                  // Store comments within each article
                  article.comments = comments;
                });
              }
            });
          })
          .catch(error => {
            console.error('Error fetching articles:', error);
          });
      },
      fetchCategories() {
        console.log("Fetching categories...");
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
        console.log("Filtering category:", categoryId);
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

      // Method to post a comment
      postComment(articleId: number, content: string) {
        console.log("Posting comment for article:", articleId);
        // Post a comment for the provided articleId
        fetch(`http://localhost:8000/api/articles/${articleId}/create_comment/`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
          },
          body: JSON.stringify({
            article_id: articleId,
            content: content,
          }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            console.log('Comment posted:', data);

            const newComment: Comment = {
              id: data.comment_id,
              content: content,
              userId: Number(this.userID),
              articleId: articleId,
              createdAt: data.created_at,
            };
            const articleIndex = this.articles.findIndex(article => article.id === articleId);
            if (articleIndex !== -1) {
              // Update the local data with the new comment
              this.articles[articleIndex].comments.push(newComment);
            }
          })
          .catch(error => {
            console.error('Error posting comment:', error);
          });
      },

      // Method to fetch comments for an article
      async fetchComments(articleId: number): Promise<Comment[]> {
        console.log("Fetching comments for article:", articleId);
        try {
          const response = await fetch(`http://localhost:8000/api/articles/${articleId}/comments/`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          return data.comments;
        } catch (error) {
          console.error('Error fetching comments:', error);
          return []; // Return an empty array in case of an error
        }
      },

      // Handle article selection or interaction to set the selectedArticleId
      selectArticle(articleId: string) {
        console.log("Selecting article:", articleId);
        this.selectedArticleId = articleId;
        if (this.selectedArticleId !== '') {
          // Fetch comments for the selected article after setting its ID
          const articleIdAsNumber: number = parseInt(this.selectedArticleId, 10);
          if (!isNaN(articleIdAsNumber)) {
            this.fetchComments(articleIdAsNumber);
          }
        }
      },
    }
  });
</script>

<style scoped>
  /* Styling for the overall news container */
  .news-container {
    font-family: 'Arial', sans-serif;
    padding: 20px;
    background-color: #f8f8f8;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 auto;
  }

  /* Styling for the header */
  .news-header {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 30px;
    color: #333;
  }

  /* Styling for the navigation bar */
  .nav-bar {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: center;
    background: linear-gradient(to right, #1a1a1a, #333333);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .nav-bar li {
    padding: 10px 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: white;
  }

  .nav-bar li:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  /* Styling for the articles */
  .article {
    margin-bottom: 30px;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .article-title {
    font-size: 1.8rem;
    margin-bottom: 15px;
    color: #333;
  }

  .article-content {
    color: #666;
    line-height: 1.6;
    margin-bottom: 20px;
  }

  .article-divider {
    margin: 20px 0;
    border: none;
    border-top: 1px solid #ddd;
  }

  /* Styling for comments */
  .comment-form {
    margin-bottom: 20px;
  }

  .comment-textarea {
    width: calc(100% - 40px);
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 6px;
    border: 1px solid #ddd;
    resize: vertical;
  }

  .comment-submit-btn {
    padding: 8px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .comment-submit-btn:hover {
    background-color: #45a049;
  }

  .comment-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  .comment {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 6px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .comment-content {
    color: #333;
    margin-bottom: 10px;
  }

  .comment-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }

  .comment-btn {
    padding: 6px 12px;
    background-color: #337ab7;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .comment-btn:hover {
    background-color: #286090;
  }

  .comment-edit {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }

  .comment-edit-textarea {
    width: calc(100% - 40px);
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 6px;
    border: 1px solid #ddd;
    resize: vertical;
  }

  .comment-edit-save-btn,
  .comment-edit-cancel-btn {
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .comment-edit-save-btn {
    background-color: #5cb85c;
    color: white;
  }

  .comment-edit-save-btn:hover {
    background-color: #4cae4c;
  }

  .comment-edit-cancel-btn {
    background-color: #d9534f;
    color: white;
  }

  .comment-edit-cancel-btn:hover {
    background-color: #c9302c;
  }
</style>