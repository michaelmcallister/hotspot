<template>
  <v-app>
    <v-app-bar app :elevation="1">
      <v-app-bar-title>
        <div class="d-sm-inline">
          <AppLogo />
        </div>
      </v-app-bar-title>
      <v-spacer />
      <v-btn variant="text" color="primary" to="/">Home</v-btn>
      <v-btn variant="text" color="primary" to="/explore">Explore</v-btn>
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

    <v-footer class="bg-grey-lighten-4 text-center pa-4" style="max-height: 120px;">
      <v-container>
        <div class="d-flex flex-column align-center">
          <AppLogo grey class="mb-2" />
          <div class="text-body-2 text-medium-emphasis mb-2">
            Information provided for guidance only. Always use your own judgement when parking.
          </div>
          <div class="d-flex align-center text-body-2">
            <router-link to="/contact" class="text-decoration-none text-grey">
              Contact
            </router-link>
            <span class="mx-2 text-grey">•</span>
            <span @click="showResources = true" class="text-decoration-none text-grey" style="cursor: pointer;">
              Resources
            </span>
          </div>
        </div>
      </v-container>
    </v-footer>

    <ResourcesModal
      :show="showResources"
      @close="showResources = false"
    />
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ResourcesModal from './components/ResourcesModal.vue';
import AppLogo from './components/AppLogo.vue';

const showResources = ref(false);
</script>

<style>
.v-application {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.v-main {
  flex: 1;
}

.v-footer {
  margin-top: auto !important;
}
</style>
