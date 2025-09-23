<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>
        <v-icon class="mr-1">mdi-motorbike</v-icon>
        Hotspot
      </v-app-bar-title>
      <v-spacer />
      <v-btn variant="text" color="primary" to="/">Home</v-btn>
      <v-btn variant="text" color="primary" to="/top-suburbs">Top Suburbs</v-btn>
      <v-btn variant="text" color="primary" to="/saved">Saved</v-btn>
      <v-btn variant="text" color="primary" to="/contact">Contact</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
</script>

