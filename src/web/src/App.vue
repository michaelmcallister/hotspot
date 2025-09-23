<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>
        <Logo />
      </v-app-bar-title>
      <v-spacer />
      <v-btn variant="text" color="primary" to="/">Home</v-btn>
      <v-btn variant="text" color="primary" to="/top-suburbs">Top Suburbs</v-btn>
      <v-btn variant="text" color="primary" to="/saved">Saved</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <v-footer color="blue-grey-lighten-4" app>
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="auto">
            <Logo size="24" text-class="text-h6 text-grey-darken-1" icon-class="text-grey-darken-1" />
          </v-col>
        </v-row>
        <v-row align="center" justify="center" class="mt-n2">
          <v-col cols="auto">
            <p class="text-center text-body-2 text-grey-darken-1 mb-0">
              Information provided for guidance only. Always use your own judgment when parking.
            </p>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import Logo from './components/Logo.vue'
</script>

