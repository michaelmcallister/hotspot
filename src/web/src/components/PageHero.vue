<template>
  <v-row justify="center">
    <v-col cols="12" lg="10" xl="8">
      <v-card
        rounded="xl"
        elevation="2"
        color="grey-lighten-5"
        class="pt-3 pt-sm-4 pt-md-6 px-6 px-sm-8 px-md-12 pb-4 pb-sm-6 pb-md-8 mt-3 mt-sm-5 mb-3 mb-md-5 text-center"
      >
        <v-card-title class="pa-0 mb-4">
          <div class="d-flex d-sm-none flex-column align-center">
            <v-avatar
              size="48"
              class="mb-3"
              color="primary"
              variant="tonal"
            >
              <v-icon size="28" color="primary">{{ icon }}</v-icon>
            </v-avatar>
            <span class="hero-title text-h4 text-sm-h3 font-weight-bold text-high-emphasis text-center">
              {{ title }}
            </span>
          </div>

          <div class="d-none d-sm-flex align-center justify-center">
            <v-avatar
              size="48"
              class="mr-4"
              color="primary"
              variant="tonal"
            >
              <v-icon size="28" color="primary">{{ icon }}</v-icon>
            </v-avatar>
            <span class="hero-title text-h3 font-weight-bold text-high-emphasis">
              {{ title }}
            </span>
          </div>
        </v-card-title>

        <div class="text-caption text-sm-body-1 text-medium-emphasis mb-3 mb-sm-4 px-2">
          {{ subtitle }}
        </div>

        <v-divider
          class="mx-auto mb-4 mb-sm-6"
          :class="{ 'mb-sm-8': !$slots.default }"
          color="primary"
          thickness="3"
          length="100"
          style="max-width: 140px;"
        />

        <v-card-text v-if="$slots.default" class="pa-0">
          <slot />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
  icon: string
}>()
</script>

<style scoped>
.hero-title {
  white-space: normal;
  word-break: break-word;
}
</style>
