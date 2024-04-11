<template>
  <div>
    <form @submit.prevent="submitForm" id="movieForm">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" v-model="formData.title" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" class="form-control" rows="4" v-model="formData.description"></textarea>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" class="form-control" @change="handlePosterChange" />
      </div>
      <div class="form-group mb-3">
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

// Define reactive variables
const formData = ref({
  title: "",
  description: "",
  poster: null,
});

const csrfToken = ref("");

// Method to handle poster file change
const handlePosterChange = (event) => {
  formData.poster = event.target.files[0];
};

// Method to fetch CSRF token
const fetchCsrfToken = () => {
  fetch('/api/v1/csrf-token')
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch CSRF token');
      }
      return response.json();
    })
    .then(data => {
      csrfToken.value = data.csrf_token;
    })
    .catch(error => {
      console.error(error);
    });
};

// Fetch CSRF token when component is mounted
onMounted(() => {
  fetchCsrfToken();
});

// Method to submit form
const submitForm = () => {
  const headers = {
    'X-CSRFToken': csrfToken.value
  };

  fetch("/api/v1/movies", {
    method: 'POST',
    body: new FormData(movieForm),
    headers: headers
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error(error);
    });
};
</script>

<style scoped>
/* Add component-specific styles here */
</style>
