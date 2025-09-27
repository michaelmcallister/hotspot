<template>
  <v-card class="mb-3" elevation="1">
    <v-card-item class="clickable-header" @click="navigateToSuburb">
      <template #prepend>
        <v-icon color="primary">mdi-map-marker-multiple</v-icon>
      </template>

      <v-card-title class="text-body-1">
        {{ suburb.suburb }}
      </v-card-title>

      <v-card-subtitle class="text-body-2">
        {{ suburb.postcode }}
      </v-card-subtitle>

      <template #append>
        <v-chip
          v-if="suburb.parking_count !== undefined"
          size="small"
          color="grey"
          variant="flat"
          class="ml-2"
        >
          {{ suburb.parking_count }}
        </v-chip>
      </template>
    </v-card-item>

    <v-card-text class="pt-3 pb-2">
      <div class="d-flex flex-wrap gap-1 mb-3">
        <v-chip size="small" color="info" label>
          <v-icon start size="14">mdi-map-marker-distance</v-icon>
          {{ formatDistance(suburb.distance_in_meters) }}
        </v-chip>

        <v-chip
          v-if="safetyScore !== null"
          size="small"
          :color="safetyColor(safetyScore)"
          variant="tonal"
          label
        >
          <v-icon start size="14">mdi-shield-check</v-icon>
          {{ safetyLabel(safetyScore) }}
        </v-chip>

        <v-chip size="small" color="grey" variant="outlined" label>
          <v-icon start size="14">mdi-map</v-icon>
          {{ suburb.lga }}
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';

  import {
    safetyLabel,
    safetyColor,
    createSlug,
    riskToSafetyScore,
    formatDistance,
  } from '../utils';

  const router = useRouter();

  interface NearestSuburb {
    postcode: string;
    suburb: string;
    lga: string;
    distance_in_meters: number;
    parking_count?: number;
    risk_score?: number;
  }

  const props = defineProps<{
    suburb: NearestSuburb;
  }>();

  const safetyScore = computed(() => {
    if (
      props.suburb.risk_score === undefined ||
      props.suburb.risk_score === null
    ) {
      return null;
    }
    return riskToSafetyScore(props.suburb.risk_score);
  });

  const navigateToSuburb = () => {
    const slug = createSlug(props.suburb.suburb, props.suburb.postcode);
    router.push({
      name: 'suburb',
      params: { slug },
      query: { tab: 'parking-feed' },
    });
  };
</script>

<style scoped>
  .gap-1 {
    gap: 0.25rem;
  }

  .clickable-header {
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .clickable-header:hover {
    background-color: rgba(var(--v-theme-primary), 0.05);
  }
</style>
