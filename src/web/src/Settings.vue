<template>
  <v-main>
    <v-container class="pt-1 pt-md-3 pb-2 pb-md-8">
      <PageHero
        title="Settings"
        subtitle="Customize your preferences and app behaviour"
        icon="mdi-cog"
      />

      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">

          <v-card class="pa-4">
            <v-card-title class="text-h6 text-sm-h5 mb-4">Navigation Preferences</v-card-title>

            <v-card-text>
              <p class="text-body-1 mb-4 text-grey-darken-1">
                Choose your preferred navigation app for getting directions to parking locations.
              </p>

              <v-radio-group v-model="navigationApp" color="primary">
                <v-radio
                  label="Google Maps"
                  value="google"
                  class="mb-2"
                />
                <v-radio
                  label="Waze"
                  value="waze"
                  class="mb-2"
                />
              </v-radio-group>

              <v-btn
                color="primary"
                variant="flat"
                size="large"
                rounded="lg"
                @click="saveSettings"
                class="mt-4"
              >
                Save Settings
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-snackbar
      v-model="showSaveMessage"
      timeout="3000"
      color="success"
      location="bottom"
      class="text-center"
    >
      <p>Settings saved successfully!</p>
    </v-snackbar>
  </v-main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageHero from './components/PageHero.vue'

const navigationApp = ref('google')
const showSaveMessage = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('navigationApp')
  if (saved) {
    navigationApp.value = saved
  }
})

const saveSettings = () => {
  localStorage.setItem('navigationApp', navigationApp.value)
  showSaveMessage.value = true
}
</script>
