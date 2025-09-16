<template>
  <div class="not-found">
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <p>Sorry, the page you're looking for doesn't exist.</p>
    <v-btn color="primary" variant="flat" size="large" rounded="lg" to="/">
      Go to Homepage
    </v-btn>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 2rem;
}

.not-found h1 {
  font-size: 6rem;
  margin: 0;
  color: #333;
}

.not-found h2 {
  font-size: 2rem;
  margin: 1rem 0;
  color: #666;
}

.not-found p {
  font-size: 1.2rem;
  color: #999;
  margin: 1rem 0 2rem;
}
</style>