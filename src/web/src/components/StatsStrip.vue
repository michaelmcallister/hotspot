<template>
  <v-card
    color="primary"
    variant="elevated"
    elevation="4"
    :rounded="$vuetify.display.xs ? 'lg' : 'xl'"
    :class="{
      'py-4 py-sm-6': true,
      'px-2': $vuetify.display.xs,
      'px-4': !$vuetify.display.xs
    }"
  >
    <v-card-text class="pa-0">
      <v-container fluid class="pa-0">
        <v-row align="center" justify="center" dense>
          <v-col
            v-for="stat in stats"
            :key="stat.label"
            cols="6"
            sm="3"
            :class="stat.class"
          >
            <div class="text-center">
              <v-fade-transition appear>
                <div>
                  <div
                    class="font-weight-bold white--text mb-1"
                    :class="$vuetify.display.xs ? 'text-h5' : 'text-h4 text-sm-h3'"
                  >
                    <v-icon
                      v-if="stat.icon && !$vuetify.display.xs"
                      size="x-small"
                      class="mr-1 mb-1"
                      color="white"
                    >
                      {{ stat.icon }}
                    </v-icon>
                    {{ stat.value }}
                  </div>
                  <div
                    class="font-weight-medium"
                    :class="$vuetify.display.xs ? 'text-caption' : 'text-caption text-sm-body-2'"
                    style="opacity: 0.9;"
                  >
                    {{ stat.label }}
                  </div>
                </div>
              </v-fade-transition>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  totalPostcodes: string | number
  totalLgas: string | number
  formattedAddresses: string
  totalSubmissions: string | number
}>()

const stats = computed(() => [
  {
    value: props.totalPostcodes,
    label: 'Postcodes',
    icon: 'mdi-map-marker'
  },
  {
    value: props.totalLgas,
    label: 'Councils',
    icon: 'mdi-city'
  },
  {
    value: props.formattedAddresses,
    label: 'Addresses',
    icon: 'mdi-home-group',
    class: 'mt-3 mt-sm-0'
  },
  {
    value: props.totalSubmissions,
    label: 'Community Spots',
    icon: 'mdi-account-multiple',
    class: 'mt-3 mt-sm-0'
  }
])
</script>