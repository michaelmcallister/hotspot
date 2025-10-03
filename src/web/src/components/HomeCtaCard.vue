<template>
  <v-card
    elevation="3"
    rounded="xl"
    class="pa-4 pa-sm-6 pa-md-8"
  >
    <v-card-text class="pa-0">
      <div class="text-center mb-4 mb-sm-6">
        <h2 class="text-h5 text-sm-h4 font-weight-bold mb-2 mb-sm-3">
          Safer Parking for Victorian Riders
        </h2>
        <p class="text-body-2 text-sm-body-1 text-medium-emphasis">
          Clear suburb safety scores and rider‑shared parking spots across Victoria.
        </p>
      </div>

      <v-row class="mb-4 mb-sm-6" justify="center" dense>
        <v-col
          v-for="(feature, index) in features"
          :key="feature.icon"
          cols="6"
          sm="3"
          class="py-1 py-sm-2"
        >
          <v-hover v-slot="{ isHovering, props }">
            <div
              v-bind="props"
              class="d-flex flex-column align-center pa-2 pa-sm-3"
              :style="{
                transform: isHovering ? 'translateY(-4px)' : 'none',
                transition: 'transform 0.2s ease'
              }"
            >
              <v-avatar
                :color="isHovering ? 'primary' : 'grey-lighten-4'"
                :size="$vuetify.display.xs ? 40 : 48"
                class="mb-2"
              >
                <v-icon
                  :color="isHovering ? 'white' : 'primary'"
                  :size="$vuetify.display.xs ? 20 : 24"
                >
                  {{ feature.icon }}
                </v-icon>
              </v-avatar>
              <div
                class="text-center"
                :class="$vuetify.display.xs ? 'text-caption' : 'text-subtitle-2'"
                style="font-weight: 500;"
              >
                {{ feature.label }}
              </div>
            </div>
          </v-hover>
        </v-col>
      </v-row>

      <div class="text-center">
        <v-btn
          @click="$emit('start-tutorial')"
          color="primary"
          variant="elevated"
          prepend-icon="mdi-play-circle-outline"
          :size="$vuetify.display.xs ? 'default' : 'x-large'"
          rounded="pill"
          :class="$vuetify.display.xs ? 'px-4' : 'px-8'"
          elevation="2"
        >
          Take a Quick Tour
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const features = [
  { icon: 'mdi-shield-check', label: 'Safety Scores' },
  { icon: 'mdi-account-group', label: 'Rider Spots' },
  { icon: 'mdi-star-outline', label: 'Favourites' },
  { icon: 'mdi-directions', label: 'Directions' }
]

defineEmits<{
  (e: 'start-tutorial'): void
}>()
</script>