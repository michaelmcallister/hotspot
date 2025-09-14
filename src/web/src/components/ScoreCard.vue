<template>
  <v-card class="mx-auto pa-6" max-width="720" elevation="6" aria-labelledby="score-title">
    <div id="score-title" class="suburb-name">{{ suburb }}</div>
    <div class="safety-score">{{ score }}</div>
    <div class="score-label">Safety Score</div>

    <v-chip :color="chipColor" variant="tonal" size="small" class="mb-4 font-weight-bold">
      {{ riskLabel }}
    </v-chip>

    <p class="description">
      Premium suburb with top-tier security and surveillance. Minimal theft risk.
    </p>
  </v-card>
  
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { safetyLabel, safetyColor } from '../utils/safety'

const props = defineProps<{
  suburb: string
  score: number
}>();

const riskLabel = computed(() => safetyLabel(props.score))
const chipColor = computed(() => safetyColor(props.score))
</script>

<style scoped>
.score-card .suburb-name {
  color: #111827;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: .25rem;
}
.safety-score {
  color: #059669;
  font-size: 3.25rem;
  font-weight: 800;
  margin: .25rem 0 0;
}
.score-label {
  color: #6b7280;
  margin-bottom: .6rem;
}

.description {
  color: #4b5563;
  line-height: 1.6;
  margin: 0 auto;
  max-width: 560px;
  background: #f9fafb;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  border-left: 4px solid #10b981;
}
</style>
