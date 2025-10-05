<template>
  <v-row justify="center" class="mb-0">
    <v-col cols="12" sm="11" md="10" lg="10" xl="8">
      <v-card
        rounded="xl"
        elevation="0"
        variant="flat"
        :class="{
          'pa-4 pa-sm-6 pa-md-8': true,
          'mt-2 mb-1': $vuetify.display.xs,
          'mt-3 mb-2': $vuetify.display.smAndUp,
          'text-center': true
        }"
      >
        <v-card-title class="pa-0 mb-3 mb-sm-4 d-flex justify-center">
          <div class="d-flex flex-column flex-sm-row align-center">
            <v-avatar
              :size="$vuetify.display.xs ? 48 : 56"
              :class="{
                'mb-2': $vuetify.display.xs,
                'mr-3': $vuetify.display.smAndUp
              }"
              color="primary"
              variant="tonal"
            >
              <v-icon
                :size="$vuetify.display.xs ? 28 : 32"
                color="primary"
              >
                {{ icon }}
              </v-icon>
            </v-avatar>
            <h1
              :class="{
                'text-h5': $vuetify.display.xs,
                'text-h4': $vuetify.display.sm,
                'text-h3': $vuetify.display.mdAndUp,
                'font-weight-bold': true
              }"
            >
              {{ title }}
            </h1>
          </div>
        </v-card-title>

        <v-card-subtitle
          class="pa-0 mb-3 mb-sm-4"
          :class="{
            'text-body-2': $vuetify.display.xs,
            'text-body-1': $vuetify.display.smAndUp,
            'text-medium-emphasis': true
          }"
        >
          <div class="mx-auto px-2" :style="{ maxWidth: $vuetify.display.xs ? '100%' : '700px' }">
            {{ subtitle }}
          </div>
        </v-card-subtitle>

        <v-divider
          v-if="showDivider && !$vuetify.display.xs"
          class="mx-auto mb-3 mb-sm-4"
          color="primary"
          thickness="3"
          style="max-width: 100px; opacity: 0.5;"
        />

        <v-card-text v-if="$slots.default" class="pa-0">
          <slot />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { computed, useSlots } from 'vue'

defineProps<{
  title: string
  subtitle: string
  icon: string
}>()

const slots = useSlots()
const showDivider = computed(() => !!slots.default)
</script>