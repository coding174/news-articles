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
    <div v-for="article in filteredArticles" :key="article.id">
      <h2>{{ article.title }}</h2>
      <p>{{ article.content }}</p>
      <hr />
      <!-- Place the comment form after each article -->
      <form @submit.prevent="submitComment(getArticleId(article))">
        <textarea v-model="articleComments[article.id]" placeholder="Type your comment here"></textarea>
        <button type="submit">Submit Comment</button>
      </form>
      <!-- comments -->
      <li v-for="comment in article.comments" :key="comment.id">
        <div v-if="!comment.editing">
          <span>{{ comment.content }}</span>
          <div v-if="showButtons(comment)">
            <button @click="editComment(comment)">Edit</button>
            <button @click="deleteComment(article, comment)">Delete</button>
          </div>
          <button @click="doReply(comment)">Reply</button>
        </div>
        <div v-else>
          <textarea v-model="comment.updatedContent" placeholder="Edit your comment"></textarea>
          <button @click="saveEditedComment(article, comment)">Save</button>
          <button @click="cancelEdit(comment)">Cancel</button>
        </div>
        <div v-if="comment.id === replyingToCommentId">
        <textarea v-model="replyContent" placeholder="Type your reply here"></textarea>
        <button @click="submitReply(comment)">Submit Reply</button>
        <button @click="cancelReply()">Cancel</button>
      </div>
      </li>
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
      const userID = ref<number | undefined>(userStore.user?.id);
      // Call fetchUserInfo when the component is mounted or when the user logs in
      onMounted(async () => {
        console.log("Component mounted");

        try {
          // Use 'await' to wait for the asynchronous operation to complete
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
        replyContent: '',
        replyMode: ref(false),
        replyingToCommentId: ref<number | null>(null),
      };
    },
    mounted() {
      console.log("Component2 mounted");
      // Fetch articles and categories from Django backend and set the data
      this.fetchArticles();
      this.fetchCategories();
      //this.fetchComments(articleId);
    },
    methods: {
      showButtons(comment: Comment) {
        return this.userID === Reflect.get(comment, 'user_id') || this.userID === Reflect.get(comment, 'userId');
      },

      editComment(comment: Comment) {
        console.log("HELL:LLL", this.userID, Reflect.get(comment, 'user_id'))
        console.log(comment)
        if (this.userID === Reflect.get(comment, 'user_id') || this.userID === Reflect.get(comment, 'userId')){
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

          // Assuming an API call is made to update the comment content
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
              // Optionally, handle the error case
            });
        } else {
          console.error('Empty comment. Cannot update.');
          // Optionally, handle the empty comment case
        }
      },

      deleteComment(article: Article, comment: Comment) {
        if (this.userID === Reflect.get(comment, 'user_id') || this.userID === Reflect.get(comment, 'userId'))
        {console.log("Deleting comment:", comment.id);
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
          });}
      },

      getArticleId(article: Article): number {
        return typeof article.id === 'string' ? parseInt(article.id, 10) : article.id;
      },

      submitComment(articleId: number) {
        console.log("Submitting comment for article:", articleId);
        if (this.articleComments[articleId] && this.articleComments[articleId].trim() !== '') {
          this.postComment(articleId, this.articleComments[articleId]);
          // Optionally, reset the form after submission
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
            // Add the new comment to the local data
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
      doReply(comment: { id: number; content: string; userId: number; articleId: number; createdAt: { toString: () => string; toDateString: () => string; }; editing?: boolean | undefined; updatedContent?: string | undefined; }) {
      this.replyMode = true;
      this.replyingToCommentId = comment.id;
      this.replyContent = ''; // Reset the reply content
      
      },
      submitReply(comment: { id: number; content: string; userId: number; articleId: number; createdAt: { toString: () => string; toDateString: () => string; }; editing?: boolean | undefined; updatedContent?: string | undefined; }) {
        console.log("Submitting reply to comment ID:", comment.id);

  // Define the API URL for posting replies
        const postReplyApiUrl = `http://localhost:8000/api/post_reply/${comment.id}/`;

  // Prepare the data for the reply
        const replyData = {
          content: this.replyContent,
    // Include any other necessary data
  };

  // Make an AJAX request to post the reply
      fetch(postReplyApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),  // Make sure you have a function to get CSRF token
        },
        body: JSON.stringify(replyData),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Reply posted:', data);
        // Handle the successful posting of the reply
        // For example, add the reply to the comments in the UI
      })
      .catch(error => {
        console.error('Error posting reply:', error);
      });

      // Reset the reply state
      this.replyMode = false;
      this.replyingToCommentId = null;
      this.replyContent = '';
      },
      cancelReply() {
      this.replyMode = false;
      this.replyingToCommentId = null;
      this.replyContent = ''; // Reset the reply content
      },
    }
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