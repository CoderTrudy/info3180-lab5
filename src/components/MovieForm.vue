<template>
    <div>
      <form @submit.prevent="saveMovie" id="movieForm">
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
  import { ref } from "vue";
  
  // Define reactive variables
  const formData = ref({
    title: "",
    description: "",
    poster: null,
  });
  
  // Method to handle poster file change
  const handlePosterChange = (event) => {
    formData.poster = event.target.files[0];
  };
  

// Method to save movie
const saveMovie = () => {
  const url = "/api/v1/movies";
  const method = "POST";
  const body = new FormData();
  body.append("title", formData.title);
  body.append("description", formData.description);
  body.append("poster", formData.poster);

  fetch(url, {
    method: method,
    body: body,
  })
    .then((response) => response.json())
    .then((data) => {
      // Display a success message
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};
</script>
<style scoped>
  /* Add component-specific styles here */
</style>
  

  
