<template>
  <v-app>
    <v-app-bar app :elevation="1">
      <v-app-bar-title>
        <v-icon class="mr-1 d-sm-inline">mdi-motorbike</v-icon>
        <span class="d-none d-sm-inline">Hotspot</span>
      </v-app-bar-title>
      <v-spacer />
      <v-btn variant="text" color="primary" to="/">Home</v-btn>
      <v-btn variant="text" color="primary" to="/top-suburbs">Top Suburbs</v-btn>
      <v-btn variant="text" color="primary" to="/saved">Saved</v-btn>

      <template v-slot:append>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi-dots-vertical" color="primary" v-bind="props"></v-btn>
          </template>
          <v-list>
            <v-list-item @click="showResources = true">
              <v-list-item-title class="text-button text-primary">Resources</v-list-item-title>
            </v-list-item>
            <v-list-item to="/settings">
              <v-list-item-title class="text-button text-primary">Settings</v-list-item-title>
            </v-list-item>
            <v-list-item to="/contact">
              <v-list-item-title class="text-button text-primary">Contact</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <ResourcesModal
      :show="showResources"
      @close="showResources = false"
    />
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ResourcesModal from './components/ResourcesModal.vue';

const showResources = ref(false);
</script>

