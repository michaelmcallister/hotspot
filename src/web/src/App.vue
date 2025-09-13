<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>
        <v-icon icon="mdi-motorbike" class="mr-2" />
        Motorcycle Hotspot
      </v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" permanent rail>
      <v-list nav density="comfortable">
        <v-list-item to="/" prepend-icon="mdi-view-dashboard" title="Dashboard" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { useTheme } from "vuetify";
import { ref } from "vue";

const drawer = ref(true);
</script>
