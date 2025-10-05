<template>
  <v-app>
    <v-layout>
      <v-app-bar app :elevation="1">
        <v-app-bar-title>
          <div class="d-sm-inline">
            <AppLogo compact />
          </div>
        </v-app-bar-title>
        <v-spacer />
        <v-btn class="d-none d-sm-inline-flex" variant="text" color="primary" to="/">Home</v-btn>
        <v-btn variant="text" color="primary" to="/explore">Explore</v-btn>
        <v-btn variant="text" color="primary" to="/saved">Your Spots</v-btn>

        <template v-slot:append>
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn icon="mdi-dots-vertical" color="primary" v-bind="props"></v-btn>
            </template>
            <v-list>
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

      <v-main class="pb-12 pb-sm-14">
        <TipsBanner v-if="route.path === '/'" />
        <router-view />
      </v-main>

      <v-footer app color="grey-lighten-5" border="t" class="py-3">
        <v-container max-width="lg">
          <v-row>
            <v-col cols="12" class="d-flex justify-center">
              <AppLogo grey class="mb-1" />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="text-center">
              <div class="text-body-2 text-medium-emphasis mb-1">
                Information provided for guidance only. Always use your own judgement when parking.
              </div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="d-flex justify-center flex-wrap">
              <v-btn to="/contact" variant="text" density="compact" size="small" class="text-grey-darken-1" aria-label="Contact">
                Contact
              </v-btn>
              <v-btn to="/privacy" variant="text" density="compact" size="small" class="text-grey-darken-1 ml-2" aria-label="Privacy Policy">
                Privacy Policy
              </v-btn>
              <v-btn variant="text" density="compact" size="small" class="text-grey-darken-1 ml-2" @click="showResources = true" aria-label="Resources">
                Resources
              </v-btn>
              <v-btn variant="text" density="compact" size="small" class="text-grey-darken-1 ml-2" @click="goToFAQ" aria-label="FAQ">
                FAQ
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-footer>

      <ResourcesModal
        :show="showResources"
        @close="showResources = false"
      />
    </v-layout> <!-- Added closing tag here -->
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ResourcesModal from './components/ResourcesModal.vue';
import AppLogo from './components/AppLogo.vue';
import TipsBanner from './components/TipsBanner.vue';

const router = useRouter();
const route = useRoute();
const showResources = ref(false);

const goToFAQ = () => {
  router.push({ name: 'faq' }); 
};
</script>