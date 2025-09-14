<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>
        <v-icon class="mr-1">mdi-motorbike</v-icon>
        Hotspot
      </v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <Homepage />
      </v-container>
    </v-main>
  </v-app>
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
