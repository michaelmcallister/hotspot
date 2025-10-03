<template>
  <v-container class="not-found-container d-flex align-center justify-center pa-8">
      <v-empty-state class="not-found-empty-state">
        <template v-slot:media>
          <v-icon size="120" color="grey-lighten-1">mdi-map-marker-question-outline</v-icon>
        </template>
        <template v-slot:title>
          <h1 class="text-grey not-found-title">404</h1>
          <h2 class="text-grey">Page Not Found</h2>
        </template>
        <template v-slot:text>
          <p class="text-grey">Sorry, the page you're looking for doesn't exist.</p>
        </template>
        <template v-slot:actions>
          <v-btn color="primary" variant="flat" size="large" rounded="lg" to="/">
            Go to Homepage
          </v-btn>
        </template>
      </v-empty-state>
  </v-container>
</template>

<script setup lang="ts">
</script>

<style scoped>
.not-found-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}


.not-found-title {
  font-size: 6rem;
  margin: 0;
  opacity: 0.3;
  line-height: 1;
}
</style>
