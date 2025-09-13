<template>
  <main class="container">
    <h1>Hotspot</h1>
    <Homepage />
  </main>
</template>

<script setup lang="ts">
import Homepage from './Homepage.vue';
</script>

<!-- Keep the same styles -->

<style>
:root {
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell,
    Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji",
    "Segoe UI Symbol", "Noto Color Emoji", sans-serif;
  color-scheme: light dark;
}

body {
  margin: 0;
  padding: 0;
}

.container {
  padding: 2rem;
}
</style>

